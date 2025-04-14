from django.db import models

class Invernadero(models.Model):
    id = models.AutoField(primary_key=True)
    id_edificio = models.IntegerField()  # Asumo que "id_recido" era "id_edificio"
    ubicacion = models.CharField(max_length=100)  # Sin tilde para evitar problemas
    temperatura = models.FloatField()
    humedad = models.FloatField()
    lumentes = models.FloatField()  # Iluminación en lúmenes (¿correcto?)

    def __str__(self):
        return f"Invernadero {self.id} - {self.ubicacion}"

class Racks(models.Model):  # ¡Corregido de "Facts" a "Racks"!
    id = models.AutoField(primary_key=True)
    id_invernadero = models.ForeignKey(Invernadero, on_delete=models.CASCADE)
    num_bandejas = models.IntegerField()  # ¿Número de bandejas en este rack?

    def __str__(self):
        return f"Rack {self.id} - Invernadero {self.id_invernadero_id}"

class Bandeja(models.Model):
    id = models.AutoField(primary_key=True)
    id_rack = models.ForeignKey(Racks, on_delete=models.CASCADE)  # Relación con Racks
    id_semilla = models.IntegerField()
    disponible = models.BooleanField(default=True)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    estado = models.CharField(max_length=50)  # Ej: "activa", "inactiva", etc.

    def __str__(self):
        return f"Bandeja {self.id} - Semilla {self.id_semilla}"
