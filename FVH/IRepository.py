from django.db import models

class BaseRepository:
    def __init__(self, model=None):
        if not model or not issubclass(model, models.Model):
            raise ValueError("Model must be a subclass of Django's models.Model")
        self.model = model

    def find_all(self):
        return self.model.objects.all()

    def save(self, entity):
        instace = self.model.objects.create(**entity)
        return instace

    def delete(self, id,user):
        return self.model.objects.filter(id=id, user_id=user).first()

    def update(self, id, data):
        return self.model.objects.filter(id=id).update(**data)

    def find_by_id(self, id):
        return self.model.objects.filter(id=id).first()
