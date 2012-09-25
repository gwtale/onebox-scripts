from django.db import models


class Url(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.IntegerField()
    country = models.CharField(max_length=20)
    time = models.CharField(max_length=1)
    
