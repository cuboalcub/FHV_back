from django.db import models
from django.contrib.auth.models import User


class Notificacion(models.Model):
    id = models.AutoField(primary_key=True)
    usuario_id = models.ForeignKey(User, on_delete=models.CASCADE)
    mensaje = models.CharField(max_length=255)
    fecha = models.DateTimeField(auto_now_add=True)
