from django.db import models


class Setting(models.Model):
    """
    Modelo que representa un setting que se puede configurar en la aplicación.
    """

    name = models.CharField(max_length=100)
    description = models.TextField(Null=True, blank=True)
    default_value = models.TextField()

    def __str__(self):
        return self.name