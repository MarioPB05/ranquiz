from django.db import models
from .time_stamp import TimeStamped


class Client(TimeStamped):
    """Modelo que representa a un cliente"""

    name = models.CharField(max_length=100)
    surnames = models.CharField(max_length=250)
    email = models.EmailField()
    birthdate = models.DateField()
    country = models.CharField(max_length=200)
