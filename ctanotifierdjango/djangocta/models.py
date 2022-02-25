from django.db import models

# Create your models here.
class Stops(models.Model):
    stop = models.CharField(max_length=40)

    def ___str___(self):
        return self.stop
