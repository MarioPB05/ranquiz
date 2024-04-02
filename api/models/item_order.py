from django.db import models


class ItemOrder(models.Model):
    """
    Modelo que representa el orden de los items en una lista de una determinada jugada.
    """

    item = models.ForeignKey('Item', on_delete=models.DO_NOTHING)
    answer = models.ForeignKey('ListAnswer', on_delete=models.DO_NOTHING)
    order = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.item.name} - {self.answer.id}'
