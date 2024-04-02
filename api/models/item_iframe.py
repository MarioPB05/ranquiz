from django.db import models

from api.models.model_template import ModelTemplate


class ItemIframe(ModelTemplate):
    """Modelo que representa un iframe de un item"""

    url = models.URLField()
    item = models.ForeignKey('Item', on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.item.name} - {self.url}'
