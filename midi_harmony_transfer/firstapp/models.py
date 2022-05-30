from email.policy import default
from django.conf import settings
from django.db import models

class midi_data(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.CharField(max_length=80)
    completed = models.CharField(max_length=80)
    #completed = models.BooleanField(default=False)

    def _str_(self):
        return self.title