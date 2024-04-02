from django.db import models

class HighlightedList(models.Model):
    """
    Modelo que representa una lista destacada.
    """

    id_list = models.ForeignKey('List', on_delete=models.DO_NOTHING)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def __str__(self):
        return self.id_list + ' - ' + self.start_date
