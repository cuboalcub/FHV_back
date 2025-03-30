from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pedido(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)  
    semillas = models.CharField(max_length=100)
    tiempo_fin = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
