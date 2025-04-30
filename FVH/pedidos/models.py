from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Pedidos(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    tiempo_final = models.DateTimeField()
    estado = models.CharField(max_length=50)
    
class DetallePedido(models.Model):
    id = models.AutoField(primary_key=True)
    pedido_id = models.ForeignKey(Pedidos, on_delete=models.CASCADE)
    producto = models.CharField(max_length=100)
    cantidad = models.IntegerField()