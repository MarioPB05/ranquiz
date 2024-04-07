from django.db import models
from shortuuid.django_fields import ShortUUIDField

from api.models.model_template import ModelTemplate


class Category(ModelTemplate):
    """Modelo que representa una categoría."""

    name = models.CharField(max_length=100, unique=True)
    share_code = ShortUUIDField(
        length=18,
        max_length=20,
        prefix="CS",
    )

    def __str__(self):
        return self.name
