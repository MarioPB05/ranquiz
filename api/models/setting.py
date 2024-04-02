from django.db import models

from api.models.model_template import ModelTemplate


class Setting(ModelTemplate):
    """Modelo que representa un ajuste que se puede configurar en la aplicación"""

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    default_value = models.TextField()

    def __str__(self):
        return self.name
