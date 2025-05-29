from typing import override

from django.forms import model_to_dict
from ENUM_RESPONSES import Responses
from IRepository import BaseRepository
from invernadero.models import Bandeja, Invernadero, Racks
from user.models import Group, detalleGroup

class InvernaderoRepository(BaseRepository):
    def __init__(self): 
        super().__init__(Invernadero)
        
    @override
    def get_all(self, user_id):
        try:
            from user.models import detalleGroup
            detalle = detalleGroup.objects.filter(user_id=user_id).first()
        
            if not detalle or not detalle.group_id:
                return []

            invernaderos = Invernadero.objects.filter(group_id=detalle.group_id)
            return invernaderos
        except Exception as e:
            print(f"Error en get_all InvernaderoRepository: {e}")
            return []
            
    @override
    def create(self, data):
        try:
            if data.get('group_id'):
                data['group_id'] = Group.objects.get(id=data['group_id'])
            invernadero = Invernadero(**data)
            print(invernadero)
            invernadero.save()
            return invernadero
        except Exception as e:
            print(f"Error al crear Invernadero: {e}")
            return None

    def get_all_racks(self, id):
        try:
            racks = Racks.objects.filter(id_invernadero=id)
            return [ model_to_dict(rack) for rack in racks]
        except Exception as e:
            return None

    def create_rack(self, data):
        try:
            data["id_invernadero"]  = Invernadero.objects.get(id=data["id_invernadero"])
            rack = Racks(**data)
            rack.save()
            return rack
        except Exception as e:  
            return None 
        
    def get_all_bandejas(self, id):
        try:
            racks = Bandeja.objects.filter(id_rack=id)
            return [ model_to_dict(rack) for rack in racks]
        except Exception as e:
            return None
        
    def create_bandeja(self, data):
        try:
            data["id_rack"]  = Racks.objects.get(id=data["id_rack"])
            bandeja = Bandeja(**data)
            bandeja.save()
            return bandeja
        except Exception as e:  
            return None