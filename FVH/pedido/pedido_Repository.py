from typing import override
from pedido.models import Pedido
from IRepository import BaseRepository

class PedidoRepository(BaseRepository):
    def __init__(self):
        super().__init__(Pedido)

    @override
    def get_all(self, user):
        return self.model.objects.filter(id_usuario=user)