from django.db import models

from api.models.model_template import ModelTemplate


class ListLike(ModelTemplate):
    """Modelo que representa un "me gusta" en una lista"""

    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    list = models.ForeignKey('List', on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.list.name}'
