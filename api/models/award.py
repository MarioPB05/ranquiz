from django.db import models

from api.models.model_template import ModelTemplate


class Award(ModelTemplate):
    """Modelo que representa un award (premio)."""

    icon = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    price = models.IntegerField()

    """
    El ToString devuelve el titulo del premio.
    """

    def __str__(self):
        return self.title
