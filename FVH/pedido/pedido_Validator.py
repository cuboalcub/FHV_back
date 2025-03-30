from pedido.models import Pedido
from IValidator import IValidator

class PedidoValidator(IValidator):
     def __init__(self):
        super().__init__(Pedido)
