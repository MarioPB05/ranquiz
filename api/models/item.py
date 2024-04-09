from cloudinary.models import CloudinaryField
from django.db import models

from api.models.model_template import ModelTemplate, IMAGE_VALIDATORS


class Item(ModelTemplate):
    """Modelo que representa un item de una lista"""

    list = models.ForeignKey('List', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    image = CloudinaryField('image', null=True, blank=True)

    def __str__(self):
        return self.name
