from django.db import models


class ModelTemplate(models.Model):
    """Modelo abstracto que establece las propiedades básicas de los modelos de la aplicación"""

    class Meta:
        app_label = 'api'
        abstract = True
