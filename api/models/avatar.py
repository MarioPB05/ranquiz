from django.db import models


class Avatar(models.Model):
    """
    Modelo que representa un avatar para un usuario
    """
    title = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='avatars/')

    def __str__(self):
        return self.title + ' (' + str(self.price) + ')'
