from typing import override

from user.user_Repository import UserRepository
from .pedido_Repository import PedidoRepository
from .pedido_Validator import PedidoValidator
from django.contrib.auth.models import User
from .models import Pedido
from IService import IService
from django.forms.models import model_to_dict
from ENUM_RESPONSES import Responses
from JWTservice import JWTService

class PedidoService(IService):
    model = Pedido  
    repository = PedidoRepository()
    userRespository = UserRepository()
    validator = PedidoValidator()
    
    def __init__(self):
        super().__init__(model=self.model, repository=self.repository)

    @override
    def get_all(self,user_id):
        try:
            pedido = self.repository.get_all(user_id)
            return {"status": Responses.OK.value, "data": pedido}
        except Exception as e:
            return {"status": Responses.INTERNAL_SERVER_ERROR.value}
    
    @override
    def add(self, data):
        try:
            data['id_usuario'] = self.userRespository.find_by_id(data['id_usuario'])
            self.repository.save(data)
            return {"status": Responses.CREATED.value, "data": self.repository.add(data)}
        except Exception as e:
            return {"status": Responses.ERROR.value, "data": str(e)}

    @override
    def update(self, data):
        data = model_to_dict(data)
        data['id_usuario'] = self.userRespository.find_by_id(data['id_usuario'])
        return self.repository.update(data)

    @override
    def delete(self, data):
        data = model_to_dict(data)
        data['id_usuario'] = self.userRespository.find_by_id(data['id_usuario'])
        return self.repository.delete(data)

    @override
    def get(self, data):
        data = model_to_dict(data)
        data['id_usuario'] = self.userRespository.find_by_id(data['id_usuario'])
        return self.repository.get(data)

