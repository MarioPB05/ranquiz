from django.db import models
from shortuuid.django_fields import ShortUUIDField

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
    share_code = ShortUUIDField(
        length=18,
        max_length=20,
        prefix="NT",
    )

    def __str__(self):
        return self.share_code
