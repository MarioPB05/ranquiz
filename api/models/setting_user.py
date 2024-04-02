from django.db import models

from api.models.model_template import ModelTemplate


class SettingUser(ModelTemplate):
    """Modelo que representa el valor de un ajuste para un usuario específico"""

    setting = models.ForeignKey('Setting', on_delete=models.DO_NOTHING)
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    value = models.CharField(max_length=800)

    def __str__(self):
        return self.user.username + ' - ' + self.setting.name
