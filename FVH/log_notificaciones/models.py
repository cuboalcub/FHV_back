from django.db import models
from user.models import Group

# class Notificacion(models.Model):
#     id = models.AutoField(primary_key=True)
#     group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
#     mensaje = models.CharField(max_length=255)
#     fecha = models.DateTimeField(auto_now_add=True)
