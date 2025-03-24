from django.db import models

class PickedNumber(models.Model):
    number = models.IntegerField(unique=True)
    user = models.CharField(max_length=100, blank=True, null=True)
    is_picked = models.BooleanField(default=False)
    is_saved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Number {self.number} - {self.user or 'Unpicked'}"