from django.db import models

class ListCategory(models.Model):
    """
    Modelo que representa una categoría de una lista.
    """
    id_list = models.ForeignKey('List', on_delete=models.DO_NOTHING)
    id_category = models.ForeignKey('Category', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.id_list + ' - ' + self.id_category
