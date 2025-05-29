from rest_framework import serializers
from .models import Invernadero, Racks, Bandeja

class InvernaderoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invernadero
        fields = '__all__'

class RacksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Racks
        fields = '__all__'

class BandejaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bandeja
        fields = '__all__'