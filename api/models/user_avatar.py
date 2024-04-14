from django.db import models

from api.models.model_template import ModelTemplate


class UserAvatar(ModelTemplate):
    """Modelo que guarda los avatares que ha comprado un usuario"""

    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    avatar = models.ForeignKey('Avatar', on_delete=models.DO_NOTHING)
    transaction = models.ForeignKey('UserTransaction', on_delete=models.DO_NOTHING, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + ' - ' + self.avatar.name
