from django.db import models


class Goal(models.Model):
    """
    Modelo que representa el valor objetivo y la recompensa de las misiones
    """
    id_type = models.ForeignKey('GoalType', on_delete=models.DO_NOTHING, related_name='goals')
    value = models.IntegerField()
    reward = models.IntegerField()

    def __str__(self):
        return self.id_type.title
