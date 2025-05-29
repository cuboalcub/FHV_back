from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Group, detalleGroup

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'is_active',
            'is_staff',
            'is_superuser'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'is_staff': {'read_only': True}  # Evita que se asigne directamente
        }

    def create(self, validated_data):
        # Crea usuario normal o superusuario según el campo
        if validated_data.get('is_superuser', False):
            user = User.objects.create_superuser(
                username=validated_data['username'],
                email=validated_data.get('email', ''),
                password=validated_data['password']
            )
        else:
            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data.get('email', ''),
                password=validated_data['password']
            )
        return user

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class DetalleGroupSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group_id.name', read_only=True)
    username = serializers.CharField(source='user_id.username', read_only=True)

    class Meta:
        model = detalleGroup
        fields = ['id', 'group_id', 'user_id', 'group_name', 'username']