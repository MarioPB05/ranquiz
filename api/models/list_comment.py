from django.db import models

from api.models.model_template import ModelTemplate


class ListComment(ModelTemplate):
    """Modelo que representa a que lista pertenece cada comentario y quien es el autor"""

    list = models.ForeignKey('List', on_delete=models.DO_NOTHING)
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' - ' + self.list.name + ' - ' + self.comment
