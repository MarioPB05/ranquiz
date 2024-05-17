from django.db.models import F
from django.utils import timezone

from api.models import UserGoal, Goal, GoalType, Notification
from api.models.notification_type import NotificationTypes
from api.services.transaction_service import do_transaction


def get_goal(goal_id):
    """Obtener misión por ID"""
    if not goal_id:
        return None

    return Goal.objects.get(id=goal_id)


def get_active_user_goal(user, goal):
    """Obtener misión del usuario"""
    goals = get_user_active_daily_goals(user)
    return goals.filter(goal=goal).first()


def get_active_user_goal_by_type(user, goal_type_id):
    """Obtener misión del usuario por tipo"""
    user_goals = get_user_active_daily_goals(user)
    return user_goals.filter(goal__id_type__id=goal_type_id).first()


def user_completed_goal(user, goal):
    """Comprobar si el usuario ha completado la misión"""
    return get_user_active_daily_goals(user).filter(user=user, goal=goal, progress__gte=goal.value).exists()


def user_claimed_goal(user, goal):
    """Comprobar si el usuario ha reclamado la misión"""
    return get_user_active_daily_goals(user).filter(user=user, goal=goal, claimed=True).exists()


def create_user_daily_goals(user):
    """Crear misiones diarias para el usuario"""
    claim_past_completed_goals(user)
    daily_goals = get_daily_goals(user)

    for goal in daily_goals:
        UserGoal.objects.create(
            user=user,
            start_date=timezone.now().replace(hour=0, minute=0, second=0),
            end_date=timezone.now().replace(hour=23, minute=59, second=59),
            progress=0,
            claimed=False,
            goal=goal
        )


def get_daily_goals(user):
    """Obtener misiones diarias"""
    goal_types = GoalType.objects.all()
    result = []

    for goal_type in goal_types:
        # Comprobar si el usuario ha completado la misión 2 veces seguidas las veces anteriores
        num_completed = UserGoal.objects.filter(
            goal__id_type__id=goal_type.id,
            claimed=True,
            user=user,
            start_date__gte=timezone.now().replace(hour=0, minute=0, second=0) - timezone.timedelta(days=2)
        ).count()

        if num_completed >= 2:
            # Ordenar por el valor más alto
            result.append(Goal.objects.filter(id_type__id=goal_type.id).order_by('-value').first())
        else:
            # Ordenar por el valor más bajo
            result.append(Goal.objects.filter(id_type__id=goal_type.id).order_by('value').first())

    return result


def claim_past_completed_goals(user):
    """Comprobar si hay misiones no reclamadas"""
    user_goals = UserGoal.objects.filter(
        user=user,
        claimed=False,
        end_date__lt=timezone.now(),
        progress__gte=F('goal__value')
    )

    for user_goal in user_goals:
        transaction = do_transaction(user, user_goal.goal.reward, 'Recompensa de misión atrasada')

        if transaction:
            user_goal.claimed = True
            user_goal.transaction = transaction
            user_goal.save()


def get_user_active_daily_goals(user):
    """Obtener misiones diarias activas del usuario"""
    daily_goals = UserGoal.objects.filter(user=user, start_date__lte=timezone.now(), end_date__gte=timezone.now())

    if not daily_goals.exists():
        create_user_daily_goals(user)
        daily_goals = UserGoal.objects.filter(user=user, start_date__lte=timezone.now(), end_date__gte=timezone.now())

    return daily_goals


def sum_goal_progress(goal_type_id, user, value):
    """Sumar progreso a la misión"""
    user_goal = get_active_user_goal_by_type(user, goal_type_id)

    if not user_goal:
        return

    user_goal.progress += value
    user_goal.save()

    if user_completed_goal(user, user_goal.goal):
        Notification.create(1, NotificationTypes.NEW_QUEST_COMPLETED.object, user, user.share_code)
