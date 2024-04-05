from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from api.models.time_stamp import TimeStamped


class UserManager(BaseUserManager):
    def create_user(self, username, share_code, avatar, client):
        if not username:
            raise ValueError('El nombre de usuario es obligatorio')
        user = self.model(
            username=username,
            share_code=share_code,
            avatar=avatar,
            client=client
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, username, share_code, avatar, client):
        user = self.create_user(
            username=username,
            share_code=share_code,
            avatar=avatar,
            client=client
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        return self.get(username=username)


class User(AbstractBaseUser, TimeStamped):
    """Modelo que representa a un usuario"""

    username = models.CharField(max_length=50, unique=True)
    share_code = models.CharField(max_length=20, unique=True)
    avatar = models.ForeignKey('Avatar', on_delete=models.DO_NOTHING)
    client = models.ForeignKey('Client', on_delete=models.DO_NOTHING)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['share_code', 'avatar', 'client']

    def __str__(self):
        return self.username + ' (' + self.share_code + ')'
