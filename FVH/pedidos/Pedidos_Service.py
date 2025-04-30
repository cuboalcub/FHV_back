from typing import override

from django.forms import model_to_dict
from ENUM_RESPONSES import Responses
from IService import IService
from pedidos.models import DetallePedido, Pedidos
from pedidos.Pedidos_Repository import PedidosRepository

class PedidosService(IService):
    model = Pedidos
    repository = PedidosRepository()
    
    def __init__(self):
        super().__init__(model=self.model, repository=self.repository)

    @override
    def get_all(self,user_id):
        try:
            return { "data": self.repository.find_all(user_id), "status": Responses.OK.value }
        except Exception as e:
            return {  "status": Responses.INTERNAL_SERVER_ERROR.value, "data": str(e) }
    
    @override
    def add(self, data):
        try:
            return { "data": self.repository.save(data), "status": Responses.CREATED.value }
        except Exception as e:
            return { "status": Responses.INTERNAL_SERVER_ERROR.value, "data": str(e) }
    @override
    def update(self, id, data):
        entity = self.repository.find_by_id(id)
        if not entity:
            return {"status": Responses.NOT_FOUND.value}

        # Sacamos los productos del diccionario antes de cualquier uso
        productos = data.pop('productos', None)

        # Actualizamos los campos del modelo
        for key, value in data.items():
            setattr(entity, key, value)

        self.repository.update(id, entity)

        # Ahora actualizamos los productos relacionados
        if productos is not None:
            DetallePedido.objects.filter(pedido_id=entity.id).delete()
            for prod in productos:
                DetallePedido.objects.create(
                    pedido_id=entity,
                    producto=prod['producto'],
                    cantidad=prod['cantidad'],
                )

        return {"status": Responses.OK.value}
