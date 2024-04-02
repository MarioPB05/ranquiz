from django.db import models

class UserFollow(models.Model):
    """
    Modelo que representa un seguimiento de un usuario a otro.
    """

    follower = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    id_user_followed = models.ForeignKey('User', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.follower + ' ha seguido a ' + self.id_user_followed
