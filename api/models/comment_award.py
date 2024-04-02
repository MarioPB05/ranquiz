from django.db import models


class CommentAward(models.Model):
    """
    Modelo que representa un premio otorgado a un comentario
    """

    comment = models.ForeignKey('ListComment', on_delete=models.DO_NOTHING)
    award = models.ForeignKey('Award', on_delete=models.DO_NOTHING)
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment.comment + ' - ' + self.award.title + ' - ' + self.user.username
