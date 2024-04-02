from django.db import models


class Category(models.Model):
    """
    Modelo que representa una categoría.
    """

    name = models.CharField(max_length=100, unique=True)
    share_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
