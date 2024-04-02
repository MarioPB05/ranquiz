from django.db import models


class UserGoal(models.Model):
    """
    Modelo que representa el progreso de un usuario en una misión
    """

    user = models.ForeignKey('User', on_delete=models.DO_NOTHING, related_name='goals')
    goal = models.ForeignKey('Goal', on_delete=models.DO_NOTHING)
    transaction = models.ForeignKey('Transaction', on_delete=models.DO_NOTHING, null=True, blank=True)
    progress = models.IntegerField(default=0)
    claimed = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def __str__(self):
        return self.user.username + ' - ' + self.goal.id_type.title
