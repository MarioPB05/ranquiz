from django.db import models

from api.models.model_template import ModelTemplate


class TimeStamped(ModelTemplate):
    """Modelo abstracto que añade campos de fecha de creación y edición, y un campo de borrado lógico"""

    creation_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
