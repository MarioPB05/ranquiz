from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from api.models import Notification, NotificationType
from api.services.social_service import get_following


def create_notification(target, notification_type, user, share_code):
    """Crea una notificación"""
    notification = Notification(
        target=target,
        user=user,
        type=notification_type,
        share_code=share_code
    )

    notification.save()

    send_notification(user, notification)

    return notification


def get_notification_type(type_id):
    """Obtiene un tipo de notificación por su ID"""
    return NotificationType.objects.get(id=type_id)


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


def send_notification(user, notification):
    """Envía una notificación a un usuario o usuarios"""
    channel_layer = get_channel_layer()

    if notification.target == 1:
        channel_name = user.share_code
    elif notification.target == 2:
        channel_name = f'followers_{user.share_code}'
    else:
        channel_name = 'global'

    async_to_sync(channel_layer.group_send)(
        channel_name,
        {
            'type': 'send_notification',
            'target': notification.target,
            'icon': notification.type.icon,
            'title': notification.type.title,
            'description': notification.type.description,
            'share_code': notification.share_code
        }
    )
