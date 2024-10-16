from django.db import models

from api.models.model_template import ModelTemplate


class CategorySubscription(ModelTemplate):
    """Modelo que representa una suscripción de usuario a una categoría."""

    user = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    category = models.ForeignKey('Category', on_delete=models.DO_NOTHING)
    notification = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.user} - {self.category}'
