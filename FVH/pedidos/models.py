from django.db import models
from user.models import Group

# Create your models here.
class Pedidos(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=1)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    tiempo_final = models.DateTimeField()
    estado = models.CharField(max_length=50)
    
class DetallePedido(models.Model):
    id = models.AutoField(primary_key=True)
    pedido_id = models.ForeignKey(Pedidos, on_delete=models.CASCADE)
    producto = models.CharField(max_length=100)
    cantidad = models.IntegerField()