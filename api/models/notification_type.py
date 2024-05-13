from enum import Enum

from django.db import models

from api.models.model_template import ModelTemplate


class NotificationTypes(Enum):
    """Tipos de notificaciones disponibles en base de datos"""

    NEW_LIST = 1
    NEW_LIST_ON_CATEGORY = 2
    NEW_LIST_OPTIONS = 3
    NEW_LIST_LIKE = 4
    NEW_LIST_COMMENT = 5
    NEW_COMMENT_AWARD = 6
    NEW_FOLLOWER = 7
    NEW_LIST_FAVORITE = 8

    @property
    def object(self):
        """Obtiene un tipo de notificación"""
        return NotificationType.get(self)


class NotificationType(ModelTemplate):
    """Modelo que representa el tipo de notificación"""

    title = models.CharField(null=True, blank=True, max_length=100)
    icon = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    @classmethod
    def get(cls, notification_type: NotificationTypes):
        """Obtiene un tipo de notificación"""
        return cls.objects.get(id=notification_type.value)
