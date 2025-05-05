import abc
from ENUM_RESPONSES import Responses
from django.db import models  
from django.forms.models import model_to_dict


class IService(abc.ABC):
    def __init__(self, model=None, repository=None ):
        if not model or not issubclass(model, models.Model):
            raise ValueError("Model must be a subclass of Django's models.Model")
        self.model = model
        self.repository = repository 
        
        

    @classmethod
    def create(self, data):
        print(f"Data: {data}")
        entity = self.model(**data)
        self.repository.save(entity)
        return {"status": Responses.CREATED.value, "data": entity}
    
    @classmethod
    def get_all(self):
        try:
            entities = self.repository.find_all()
            return {
                "status": Responses.ACCEPTED.value,
                "data": [model_to_dict(entity) for entity in entities]  # 🔥 Convierte objetos a diccionarios
            }
        except Exception as e:
            return {"status": Responses.INTERNAL_SERVER_ERROR.value}


    @classmethod
    def get_by_id(self, id):
        try:
            entity = self.repository.find_by_id( id)
            return {"status": Responses.ACCEPTED.value, "data": model_to_dict(entity)} if entity else {"status": Responses.NOT_FOUND.value}
        except Exception as e:
            print(f"Error: {e}")
            return {"status": Responses.INTERNAL_SERVER_ERROR.value, "error": str(e)}

    @classmethod
    def add(self, data):
        instance = self.repository.save(data)
        return {"status": Responses.CREATED.value, "data": instance}

    @classmethod
    def delete(self, id,user):
        entity = self.repository.find_by_id(id)
        if not entity:
            return {"status": Responses.NOT_FOUND.value}
        entity = self.repository.delete(id,user)
        entity.delete()
        if entity == 0:
            return {"status": Responses.NOT_FOUND.value}
        return {"status": Responses.OK.value}

    @classmethod
    def update(self, id, data):
        entity = self.repository.find_by_id(id)
        if not entity:
            return {"status": Responses.NOT_FOUND.value}

        entity_dict = model_to_dict(entity)
        temp_entity = self.model(**{**entity_dict, **data})

        for key, value in data.items():
            setattr(entity, key, value)

        self.repository.update(id, entity)
        return {"status": Responses.OK.value}
