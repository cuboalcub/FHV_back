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
        
    @override
    def get_all(self, user_id):
        try:
            invernaderos = self.repository.get_all(user_id)
            return {"status" : Responses.OK.value , "data": [model_to_dict(i) for i in invernaderos]}
        except Exception as e:
            return Responses.INTERNAL_SERVER_ERROR.value
        
        
    @override
    def create(self, data):
        try:
            invernadero = self.repository.create(data)
            print(invernadero)
            return {"status" : Responses.OK.value}
        except Exception as e:
            return Responses.INTERNAL_SERVER_ERROR.value
        
    def get_all_racks(self, id):
        try:
            racks = self.repository.get_all_racks(id)
            return {"status" : Responses.OK.value , "data": racks}
        except Exception as e:
            return Responses.INTERNAL_SERVER_ERROR.value
        
    def create_rack(self, data):
        try:
            rack = self.repository.create_rack(data)
            return {"status" : Responses.OK.value, "data": model_to_dict(rack)}
        except Exception as e:
            return Responses.INTERNAL_SERVER_ERROR.value
        
        
    def get_all_bandejas(self, id):
        try:
            bandejas = self.repository.get_all_bandejas(id)
            return {"status" : Responses.OK.value , "data": bandejas}
        except Exception as e:
            return Responses.INTERNAL_SERVER_ERROR.value
        
    def create_bandeja(self, data):
        try:
            bandeja = self.repository.create_bandeja(data)
            return {"status" : Responses.OK.value, "data": model_to_dict(bandeja)}
        except Exception as e:  
            return Responses.INTERNAL_SERVER_ERROR.value