from typing import override
from rest_framework.exceptions import ValidationError
from ENUM_RESPONSES import Responses
from IService import IService
from invernadero.models import Invernadero, Racks, Bandeja
from invernadero.Invernadero_Repository import InvernaderoRepository
from invernadero.serializers import InvernaderoSerializer, RacksSerializer, BandejaSerializer

class InvernaderoService(IService):
    model = Invernadero
    repository = InvernaderoRepository()

    def __init__(self):
        super().__init__(model=self.model, repository=self.repository)

    @override
    def get_all(self, user_id):
        try:
            invernaderos = self.repository.get_all(user_id)
            if not invernaderos:
                return {"status": Responses.NOT_FOUND.value, "error": "No invernaderos found for user's group"}

            serializer = InvernaderoSerializer(invernaderos, many=True)
            return {"status": Responses.OK.value, "data": serializer.data}

        except Exception as e:
            return {"status": Responses.INTERNAL_SERVER_ERROR.value, "error": str(e)}

    @override
    def create(self, data):
        try:
            serializer = InvernaderoSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return {"status": Responses.OK.value, "data": serializer.data}
            else:
                return {"status": Responses.INTERNAL_SERVER_ERROR.value, "error": serializer.errors}
        except Exception as e:
            return {"status": Responses.INTERNAL_SERVER_ERROR.value, "error": str(e)}

    def get_all_racks(self, id):
        try:
            racks = self.repository.get_all_racks(id)
            serializer = RacksSerializer(racks, many=True)
            return {"status": Responses.OK.value, "data": serializer.data}
        except Exception as e:
            return {"status": Responses.INTERNAL_SERVER_ERROR.value, "error": str(e)}

    def create_rack(self, data):
        try:
            serializer = RacksSerializer(data=data)
            if serializer.is_valid():
                rack = serializer.save()
                return {"status": Responses.OK.value, "data": RacksSerializer(rack).data}
            else:
                return {"status": Responses.INTERNAL_SERVER_ERROR.value, "error": serializer.errors}
        except Exception as e:
            return {"status": Responses.INTERNAL_SERVER_ERROR.value, "error": str(e)}

    def get_all_bandejas(self, id):
        try:
            bandejas = self.repository.get_all_bandejas(id)
            serializer = BandejaSerializer(bandejas, many=True)
            return {"status": Responses.OK.value, "data": serializer.data}
        except Exception as e:
            return {"status": Responses.INTERNAL_SERVER_ERROR.value, "error": str(e)}

    def create_bandeja(self, data):
        try:
            serializer = BandejaSerializer(data=data)
            if serializer.is_valid():
                bandeja = serializer.save()
                return {"status": Responses.OK.value, "data": BandejaSerializer(bandeja).data}
            else:
                return {"status": Responses.INTERNAL_SERVER_ERROR.value, "error": serializer.errors}
        except Exception as e:
            return {"status": Responses.INTERNAL_SERVER_ERROR.value, "error": str(e)}