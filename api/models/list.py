from api.models.time_stamp import *


class List(TimeStamped):
    """
    Modelo que representa una lista jugable
    """

    TYPE_CHOICES = (
        (0, 'Normal'),
        (1, 'Spotify'),
        (2, 'Youtube'),
    )

    owner = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    share_code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    public = models.BooleanField(default=False)
    image = models.ImageField(upload_to='lists/', null=True, blank=True)
    type = models.IntegerField(choices=TYPE_CHOICES, default=0)

    def __str__(self):
        return self.name + ' (' + self.share_code + ')'
