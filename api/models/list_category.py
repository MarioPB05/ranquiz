from django.db import models


class ListCategory(models.Model):
    """
    Modelo que representa una categoría de una lista.
    """

    list = models.ForeignKey('List', on_delete=models.DO_NOTHING)
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.list.name + ' - ' + self.category.name
