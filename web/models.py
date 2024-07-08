from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length = 50)
    init = models.DateTimeField(null = True)
    minutes = models.IntegerField(default = 0)
    real_init = models.DateTimeField(null = True)
    user = models.ForeignKey(User, on_delete = models.CASCADE) 

    
class Record(models.Model):
    name = models.CharField(max_length = 50)
    date = models.DateTimeField(null = True)
    minutes = models.IntegerField(default = 0)
    user = models.ForeignKey(User, on_delete = models.CASCADE) 
