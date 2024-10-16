from django.db import models

from api.models.model_template import ModelTemplate


class NotificationRead(ModelTemplate):
    """Modelo que representa una notificación leída por un usuario"""

    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    notification = models.ForeignKey('Notification', on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True)
