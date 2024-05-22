from django.http import JsonResponse
from django.views.decorators.http import require_GET

from api.decorators.api_decorators import require_authenticated
from api.services.notification_service import clear_notifications


@require_GET
@require_authenticated
def clear_notifications_controller(request):
    """Controlador que limpia las notificaciones"""
    user = request.user
    clear_notifications(user)

    return JsonResponse({'status': 'success'})
