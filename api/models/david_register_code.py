from django.db import models


class DavidRegisterCode(models.Model):
    """Modelo que representa un código de registro de David"""
    code = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code