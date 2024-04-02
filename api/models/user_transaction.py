from django.db import models


class UserTransaction(models.Model):
    """Modelo que representa una transacción de un usuario con monedas"""

    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    value = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    details = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username + ' - ' + str(self.value) + ' - ' + self.details
