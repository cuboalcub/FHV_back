from django.db import models
from user.models import Group
from pedidos.models import DetallePedido
class Invernadero(models.Model):
    id = models.AutoField(primary_key=True)
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True, default=1)  
    ubicacion = models.CharField(max_length=100)
    num_bandejas = models.IntegerField()  # 
    
    

class Racks(models.Model):  # ¡Corregido de "Facts" a "Racks"!
    id = models.AutoField(primary_key=True)
    id_invernadero = models.ForeignKey(Invernadero, on_delete=models.CASCADE)
    num_bandejas = models.IntegerField()  # ¿Número de bandejas en este rack?

    def __str__(self):
        return f"Rack {self.id} - Invernadero {self.id_invernadero_id}"

class Bandeja(models.Model):
    id = models.AutoField(primary_key=True)
    id_rack = models.ForeignKey(Racks, on_delete=models.CASCADE)  # Relación con Racks
    pedido_id = models.ForeignKey(DetallePedido, on_delete=models.CASCADE, null=True, blank=True)  # Relación con Pedidos
    semilla = models.CharField(max_length=100, default="No hay semilla")
    peso = models.FloatField(default=0)
    fecha_fin = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=50)  # Ej: "activa", "inactiva", etc.

