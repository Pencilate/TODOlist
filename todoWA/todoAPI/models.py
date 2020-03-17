from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Todo(models.Model):
    #Model for one TODO object
    # todoID = models.IntegerField(primary_key=True, auto_created=True)
    createdBy = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=1024)
    status = models.BooleanField()
