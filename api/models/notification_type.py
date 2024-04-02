from django.db import models


class NotificationType(models.Model):
    """Modelo que representa el tipo de notificación"""

    tittle = models.CharField(Null=True, blank=True, max_length=100)
    icon = models.CharField()
    description = models.TextField(Null=True, blank=True)

    def __str__(self):
        return self.tittle
