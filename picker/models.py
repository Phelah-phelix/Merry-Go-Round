from django.db import models

class PickedNumber(models.Model):
    number = models.IntegerField(unique=True)  # The number to be picked
    user = models.CharField(max_length=100)    # The user who picked the number
    is_picked = models.BooleanField(default=False)  # Whether the number has been picked

    def __str__(self):
        return f"{self.number} - {self.user}"