from django.db import models


class Award(models.Model):
    """
    Modelo que representa un award (premio).
    """

    icon = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    price = models.IntegerField()

    """
    El ToString devuelve el titulo del premio.
    """

    def __str__(self):
        return self.title
