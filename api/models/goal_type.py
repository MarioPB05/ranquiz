from django.db import models

from api.models.model_template import ModelTemplate


class GoalType(ModelTemplate):
    """Modelo que representa los tipos de las misiones"""

    TARGET_CHOICES = (
        (1, 'Para todos'),
        (2, 'Solo para creadores'),
        (3, 'Solo para usuarios'),
    )

    title = models.CharField(max_length=100, unique=True)
    target = models.IntegerField(choices=TARGET_CHOICES)

    def __str__(self):
        return self.title
