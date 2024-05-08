from api.models import Notification
from api.services.social_service import get_following


def get_notifications(user):
    """Obtiene las notificaciones de un usuario"""
    own_notifications = Notification.objects.filter(user=user, target=Notification.TARGET_CHOICES.DUEÑO)

    # Obtener los usuarios que sigue el usuario
    following_users = get_following(user)

    following_notifications = Notification.objects.filter(
        user__in=following_users,
        target=Notification.TARGET_CHOICES.SEGUIDORES
    )

    return own_notifications.union(following_notifications).order_by('-date')
