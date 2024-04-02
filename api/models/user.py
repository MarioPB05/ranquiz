from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from api.models.time_stamp import TimeStamped
from django.db import models


class User(AbstractBaseUser, PermissionsMixin, TimeStamped):
    """
    Modelo que representa a un usuario
    """
    username = models.CharField(max_length=50, unique=True)
    avatar = models.ForeignKey('Avatar', on_delete=models.CASCADE)
    share_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.username + ' (' + self.share_code + ')'
