from cloudinary.models import CloudinaryField
from django.db import models

from api.models.model_template import ModelTemplate


class Avatar(ModelTemplate):
    """Modelo que representa un avatar para un usuario"""

    title = models.CharField(max_length=250)
    image = CloudinaryField('image', null=True, blank=True)
    rarity = models.ForeignKey('AvatarRarity', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title + ' (' + str(self.rarity.price) + ')'
