from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

from api.models.time_stamp import TimeStamped


class User(AbstractBaseUser, TimeStamped):
    """Modelo que representa a un usuario"""

    username = models.CharField(max_length=50, unique=True)
    share_code = models.CharField(max_length=20, unique=True)
    avatar = models.ForeignKey('Avatar', on_delete=models.DO_NOTHING)
    client = models.ForeignKey('Client', on_delete=models.DO_NOTHING)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username', 'share_code', 'avatar', 'client']

    def __str__(self):
        return self.username + ' (' + self.share_code + ')'
