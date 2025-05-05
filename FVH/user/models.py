from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)


class detalleGroup(models.Model):
    id = models.AutoField(primary_key=True)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
