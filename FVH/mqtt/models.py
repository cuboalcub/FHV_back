from django.db import models
from invernadero.models import Invernadero
# Create your models here.
class Mqtt(models.Model):
    id = models.AutoField(primary_key=True)
    invernadero = models.ForeignKey(Invernadero, on_delete=models.CASCADE, null=True, blank=True)
    topic = models.CharField(max_length=255)
    payload = models.TextField()
    qos = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)