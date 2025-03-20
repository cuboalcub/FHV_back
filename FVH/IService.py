import abc
from ENUM_RESPONSES import Responses
from django.db import models  
from IValidator import IValidator
from django.forms.models import model_to_dict


class IService(abc.ABC):
    def __init__(self, model=None, repository=None, validator=None):
        if not model or not issubclass(model, models.Model):
            raise ValueError("Model must be a subclass of Django's models.Model")
        self.model = model
        self.repository = repository 
        self.validator = validator

    @classmethod
    def get_all(self):
        entities = self.model.objects.all()
        print(entities)
        return {
            "status": Responses.ACCEPTED.value,
            "data": [model_to_dict(entity) for entity in entities]  # 🔥 Convierte objetos a diccionarios
        }


    @classmethod
    def get_by_id(self, id):
        entity = self.repository.find_by_id(self.model, id)
        return {"status": Responses.ACCEPTED.value, "data": entity.to_dict()} if entity else {"status": Responses.NOT_FOUND.value}

    @classmethod
    def add(self, data):
        print(data)
        print(self.model)
        entity = self.model(**data)
        self.repository.save( entity)
        return {"status": Responses.CREATED.value}

    @classmethod
    def delete(self, id):
        if id is None:
            return {"status": Responses.BAD_REQUEST.value}

        deleted_count = self.repository.delete(self.model, id)
        if deleted_count == 0:
            return {"status": Responses.NOT_FOUND.value}
        return {"status": Responses.NO_CONTENT.value}

    @classmethod
    def update(self, id, data):
        entity = self.repository.find_by_id(self.model, id)
        if not entity:
            return {"status": Responses.NOT_FOUND.value}

        # Validación antes de modificar el objeto
        temp_entity = self.model(**{**entity.__dict__, **data})
        self.validator.validate(temp_entity)

        for key, value in data.items():
            setattr(entity, key, value)

        self.repository.update(self.model, id, entity)
        return {"status": Responses.OK.value}
