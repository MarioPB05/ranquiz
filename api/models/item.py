from django.db import models


class Item(models.Model):
    """
    Modelo que representa un item de una lista
    """

    list = models.ForeignKey('List', on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=f'{list.share_code}/items/', null=True, blank=True)

    def __str__(self):
        return self.name
