from cloudinary.models import CloudinaryField
from django.db import models
from shortuuid.django_fields import ShortUUIDField

from api.models.model_template import IMAGE_VALIDATORS
from api.models.time_stamp import TimeStamped


class List(TimeStamped):
    """Modelo que representa una lista jugable"""

    TYPE_CHOICES = (
        (0, 'Normal'),
        (1, 'Spotify'),
        (2, 'Youtube'),
    )

    owner = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    share_code = ShortUUIDField(
        length=18,
        max_length=20,
        prefix="LS",
    )
    name = models.CharField(max_length=70)
    public = models.BooleanField(default=False)
    image = CloudinaryField('image', null=True, blank=True)
    type = models.IntegerField(choices=TYPE_CHOICES, default=0)

    def __str__(self):
        return self.name + ' (' + self.share_code + ')'
