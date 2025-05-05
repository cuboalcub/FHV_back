from typing import override
from django.forms import model_to_dict
from ENUM_RESPONSES import Responses
from IService import IService
from invernadero.models import Invernadero, Racks, Bandeja
from invernadero.Invernadero_Repository import InvernaderoRepository

class InvernaderoService(IService):
    model = Invernadero
    repository = InvernaderoRepository()
    
    def __init__(self):
        super().__init__(model=self.model, repository=self.repository)