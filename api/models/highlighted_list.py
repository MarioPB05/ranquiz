from django.db import models


class HighlightedList(models.Model):
    """
    Modelo que representa una lista destacada.
    """

    list = models.ForeignKey('List', on_delete=models.DO_NOTHING)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def __str__(self):
        return self.list.name + ' - ' + self.start_date.strftime('%Y-%m-%d %H:%M:%S')
