from django.db import models

from api.models.model_template import ModelTemplate


class Item(ModelTemplate):
    """Modelo que representa un item de una lista"""

    list = models.ForeignKey('List', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='items/', null=True, blank=True)

    def __str__(self):
        return self.name
