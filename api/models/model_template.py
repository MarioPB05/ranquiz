from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

MAX_SIZE = 5 * 1024 * 1024  # 5 MB


def validate_image_size(size):
    """Validador que verifica que el tamaño de la imagen no exceda el tamaño máximo permitido"""
    if size > MAX_SIZE:
        raise ValidationError(f'El tamaño máximo permitido es de {MAX_SIZE} bytes')

    return size


IMAGE_VALIDATORS = [
    FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg']),
    validate_image_size
]


class ModelTemplate(models.Model):
    """Modelo abstracto que establece las propiedades básicas de los modelos de la aplicación"""

    class Meta:
        app_label = 'api'
        abstract = True
