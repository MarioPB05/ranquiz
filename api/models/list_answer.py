from django.db import models

from api.models.model_template import ModelTemplate


class ListAnswer(ModelTemplate):
    """Modelo que representa una jugada de un usuario a una lista"""

    list = models.ForeignKey('List', on_delete=models.DO_NOTHING)
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
        return self.user.username + ' - ' + self.list.name
