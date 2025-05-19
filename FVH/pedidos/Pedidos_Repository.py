from typing import override
from ENUM_RESPONSES import Responses
from IRepository import BaseRepository
from pedidos.models import DetallePedido, Pedidos
from user.models import Group, detalleGroup

class PedidosRepository(BaseRepository):
    def __init__(self): 
        super().__init__(Pedidos)
        
    @override
    def find_all(self,id):
        try:
            
            return self.model.objects.filter(group_id=id)    
        except Exception as e:
            return Responses.ERROR.value
        
    @override
    def save(self, data):
        try:
            productos = data.pop('productos', [])
            print(data)
            user  = data.pop('user_id')
            group = detalleGroup.objects.filter(user_id=user).first()
            data['group_id'] = group.group_id.id
            print(data)
            pedido = self.model.objects.create(**data)
            for prod in productos:
                DetallePedido.objects.create(
                pedido_id=pedido,
                producto=prod['producto'],
                cantidad=prod['cantidad'],
                )
            return pedido
        except Exception as e:
            print(e)
            return Responses.INTERNAL_SERVER_ERROR.value
        
        
    @override
    def update(self, id, data):
        try:
            pedido = self.model.objects.get(id=id)
            pedido.user_id = data.pop('user_id')
            pedido.save()
            print("Pedido actualizado")
            return pedido
        except Exception as e:    
            return Responses.INTERNAL_SERVER_ERROR.value    
        