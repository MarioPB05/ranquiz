from django.db import models


class Notification(models.Model):
    """Modelo que representa una notificación que se puede enviar a los usuarios"""

    TARGET_CHOICES = (
        (1, 'Dueño'),
        (2, 'Seguidores'),
        (3, 'Global'),
    )

    target = models.IntegerField(choices=TARGET_CHOICES)
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    type = models.ForeignKey('NotificationType', on_delete=models.DO_NOTHING)
    share_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.share_code
