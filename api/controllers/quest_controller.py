from django.http import JsonResponse
from django.views.decorators.http import require_GET

from api.decorators.api_decorators import require_authenticated
from api.services.goal_service import get_goal, user_completed_goal, user_claimed_goal, get_active_user_goal
from api.services.transaction_service import do_transaction


@require_GET
@require_authenticated
def claim_quest_reward(request):
    """Controlador para reclamar la recompensa de una misión"""
    goal_id = request.GET.get('goal')
    goal = get_goal(goal_id)

    if not goal:
        return JsonResponse({'status': 'error', 'message': 'Misión no encontrada'})

    if not user_completed_goal(request.user, goal):
        return JsonResponse({'status': 'error', 'message': 'Misión no completada'})

    if user_claimed_goal(request.user, goal):
        return JsonResponse({'status': 'error', 'message': 'Misión ya reclamada'})

    user_goal = get_active_user_goal(request.user, goal)
    transaction = do_transaction(request.user, goal.reward, 'Recompensa de misión')

    if not transaction:
        return JsonResponse({'status': 'error', 'message': 'Error al reclamar la recompensa'})

    user_goal.claimed = True
    user_goal.save()

    return JsonResponse({'status': 'success'})
