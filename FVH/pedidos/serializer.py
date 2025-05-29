from rest_framework import serializers
from pedidos.models import Pedidos, DetallePedido

class DetallePedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = ['id', 'producto', 'cantidad']

class PedidosSerializer(serializers.ModelSerializer):
    detalle_pedido = DetallePedidoSerializer(many=True, read_only=True, source='detallepedido_set')

    class Meta:
        model = Pedidos
        fields = ['id', 'group', 'fecha_pedido', 'tiempo_final', 'estado', 'detalle_pedido']