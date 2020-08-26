from django.db import models

# Create your models here.

class users(models.Model):
    uid = models.CharField(max_length = 100, null = False)
    habbit = models.TextField(null = False)

    def __str__(self):
        return self.uid