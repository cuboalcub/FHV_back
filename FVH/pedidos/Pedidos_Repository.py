from typing import override
from ENUM_RESPONSES import Responses
from IRepository import BaseRepository
from pedidos.models import DetallePedido, Pedidos

class PedidosRepository(BaseRepository):
    def __init__(self): 
        super().__init__(Pedidos)
        
    @override
    def find_all(self,user):
        try:
            return self.model.objects.filter(user_id=user)    
        except Exception as e:
            return Responses.ERROR.value
        
    @override
    def save(self, data):
        try:
            productos = data.pop('productos', [])
            pedido = self.model.objects.create(**data)
            for prod in productos:
                DetallePedido.objects.create(
                pedido_id=pedido,
                producto=prod['producto'],
                cantidad=prod['cantidad'],
                )
            return pedido
        except Exception as e:
            return Responses.ERROR.value
        
        
    @override
    def update(self, id, data):
        try:
            pedido = self.model.objects.get(id=id)
            pedido.user_id = data.pop('user_id')
            pedido.save()
            return pedido
        except Exception as e:    
            return Responses.INTERNAL_SERVER_ERROR.value    
        