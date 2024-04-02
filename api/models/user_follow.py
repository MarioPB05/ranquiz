from django.db import models

from api.models.model_template import ModelTemplate


class UserFollow(ModelTemplate):
    """Modelo que representa un seguimiento de un usuario a otro"""

    follower = models.ForeignKey('User', related_name='following_set', on_delete=models.DO_NOTHING)
    user_followed = models.ForeignKey('User', related_name='followers_set', on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.follower.username + ' ha seguido a ' + self.user_followed.username
