from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from shortuuid.django_fields import ShortUUIDField

from api.models.time_stamp import TimeStamped


class UserManager(BaseUserManager):
    """Manager del modelo User"""

    def create_user(self, username, share_code, avatar, client):
        """Crea un usuario"""
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
        """Crea un usuario administrador"""
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
        """Devuelve un usuario por su nombre de usuario"""
        return self.get(username=username)


class User(AbstractBaseUser, TimeStamped):
    """Modelo que representa a un usuario"""

    username = models.CharField(max_length=50, unique=True)
    share_code = ShortUUIDField(
        length=18,
        max_length=20,
        prefix="US",
    )
    avatar = models.ForeignKey('Avatar', on_delete=models.DO_NOTHING)
    client = models.ForeignKey('Client', on_delete=models.DO_NOTHING)
    is_admin = models.BooleanField(default=False)
    money = models.IntegerField(default=30)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['share_code', 'avatar', 'client']

    def has_perm(self, perm, obj=None):  # skipcq: PYL-W0613
        """Devuelve si el usuario tiene permiso"""
        return self.is_admin

    def has_module_perms(self, app_label):  # skipcq: PYL-W0613
        """Devuelve si el usuario tiene permisos para un módulo"""
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def __str__(self):
        return self.username + ' (' + self.share_code + ')'

    @classmethod
    def get(cls, user_id=None, share_code=None):
        """Función que obtiene un usuario por su id o su share_code"""
        try:
            if user_id is not None:
                return cls.objects.get(id=user_id)

            if share_code is not None:
                return cls.objects.get(share_code=share_code)

            return None
        except cls.DoesNotExist:
            return None
