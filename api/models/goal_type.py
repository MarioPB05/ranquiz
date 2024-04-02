from django.db import models


class GoalType(models.Model):
    """
    Modelo que representa los tipos de las misiones
    """
    title = models.CharField(max_length=100, unique=True)
    target = models.IntegerField()

    """
    Para quien esta dirigida (target):

    - Para todos
    - Solo para creadores
    - Solo para usuarios
    """

    def __str__(self):
        return self.title
