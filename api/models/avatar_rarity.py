from django.db import models

from api.models.model_template import ModelTemplate


class AvatarRarity(ModelTemplate):
    """Modelo que representa la rareza de un avatar y establece su precio"""

    name = models.CharField(max_length=150)
    price = models.IntegerField()

    def __str__(self):
        return self.name + ' (' + str(self.price) + ')'
