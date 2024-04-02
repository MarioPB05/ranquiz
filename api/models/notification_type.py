from django.db import models

from api.models.model_template import ModelTemplate


class NotificationType(ModelTemplate):
    """Modelo que representa el tipo de notificación"""

    tittle = models.CharField(null=True, blank=True, max_length=100)
    icon = models.CharField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.tittle
