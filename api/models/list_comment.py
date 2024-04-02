from django.db import models


class ListComment(models.Model):
    """
    Modelo que representa a que lista pertenece cada comentario y quien es el autor.
    """

    list = models.ForeignKey('List', on_delete=models.DO_NOTHING)
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    comment = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.user.username + ' - ' + self.list.name + ' - ' + self.comment
