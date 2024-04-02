from django.db import models

from api.models.model_template import ModelTemplate


class Category(ModelTemplate):
    """Modelo que representa una categoría."""

    name = models.CharField(max_length=100, unique=True)
    share_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name
