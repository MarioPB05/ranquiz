from django.db import models


class UserFollow(models.Model):
    """
    Modelo que representa un seguimiento de un usuario a otro.
    """

    follower = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    user_followed = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.follower.username + ' ha seguido a ' + self.user_followed.username
