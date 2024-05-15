from django.utils import timezone

from api.models import UserGoal, Goal


def get_goal(goal_id):
    """Obtener misión por ID"""
    if not goal_id:
        return None

    return Goal.objects.get(id=goal_id)


def get_active_user_goal(user, goal):
    """Obtener misión del usuario"""
    goals = get_user_active_daily_goals(user)
    return goals.filter(goal=goal).first()


def user_completed_goal(user, goal):
    """Comprobar si el usuario ha completado la misión"""
    return UserGoal.objects.filter(user=user, goal=goal, progress__gte=goal.value).exists()


def user_claimed_goal(user, goal):
    """Comprobar si el usuario ha reclamado la misión"""
    return UserGoal.objects.filter(user=user, goal=goal, claimed=True).exists()


def check_user_daily_goals(user):
    """Comprobar si el usuario tiene misiónes diarias"""
    return UserGoal.objects.filter(user=user, start_date__lte=timezone.now(), end_date__gte=timezone.now()).exists()


def create_user_daily_goals(user):
    """Crear misiones diarias para el usuario"""
    daily_goals = get_daily_goals()

    for goal in daily_goals:
        UserGoal.objects.create(
            user=user,
            start_date=timezone.now().replace(hour=0, minute=0, second=0),
            end_date=timezone.now().replace(hour=23, minute=59, second=59),
            progress=0,
            claimed=False,
            goal=goal
        )


def get_daily_goals():
    """Obtener misiones diarias"""
    return Goal.objects.all()


def get_user_active_daily_goals(user):
    """Obtener misiones diarias activas del usuario"""
    daily_goals = UserGoal.objects.filter(user=user, start_date__lte=timezone.now(), end_date__gte=timezone.now())

    if not daily_goals.exists():
        create_user_daily_goals(user)
        daily_goals = UserGoal.objects.filter(user=user, start_date__lte=timezone.now(), end_date__gte=timezone.now())

    return daily_goals
