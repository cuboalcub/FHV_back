import abc
from ENUM_RESPONSES import Responses
from django.db import models

class IValidator(abc.ABC):
    def __init__(self, model=None):
        if not model or not issubclass(model, models.Model):
            raise ValueError("Model must be a subclass of Django's models.Model")
        self.model = model

    @classmethod
    def validate(cls, entity):
        if not cls.model is None:
            # Obtener los campos del modelo, excluyendo 'id'
            required_fields = [field.name for field in cls.model._meta.fields if field.name != "id"]

            # Validar que todos los campos requeridos existan y no sean None o vacíos
            for field in required_fields:
                value = getattr(entity, field, None)
                if value is None or value == "":
                    return {"status": Responses.BAD_REQUEST.value, "message": f"El campo {field} es requerido"}

        raise NotImplementedError("Las clases hijas deben definir el atributo 'model'")

        return {"status": Responses.OK.value}
