from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import models

from api.models.model_template import ModelTemplate


class Notification(ModelTemplate):
    """Modelo que representa una notificación que se puede enviar a los usuarios"""

    TARGET_CHOICES = (
        (1, 'Dueño'),
        (2, 'Seguidores'),
        (3, 'Global'),
    )

    target = models.IntegerField(choices=TARGET_CHOICES)
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    type = models.ForeignKey('NotificationType', on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True)
    share_code = models.CharField(max_length=20)

    def __str__(self):
        return self.share_code

    @classmethod
    def create(cls, target: int, notification_type, user, share_code: str):
        """Crea una notificación"""
        notification = cls(
            target=target,
            user=user,
            type=notification_type,
            share_code=share_code
        )

        notification.save()

        cls.send(user, notification)

        return notification

    @classmethod
    def send(cls, user, notification):
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
