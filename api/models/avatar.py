from django.db import models


class Avatar(models.Model):
    """
    Modelo que representa un avatar para un usuario
    """

    title = models.CharField(max_length=250)
    image = models.ImageField(upload_to='avatars/')
    rarity = models.ForeignKey('AvatarRarity', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title + ' (' + str(self.rarity.price) + ')'
