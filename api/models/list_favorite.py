from django.db import models


class ListFavorite(models.Model):
    """
    Modelo que representa un favorito en una lista.
    """
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    list = models.ForeignKey('List', on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.list.name}'
