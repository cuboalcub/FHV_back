from django.db import models

# This acts as the repository
class RackManager(models.Manager):
    def get_by_id(self, rack_id):
        return self.get(id = rack_id)
    
    def get_all(self):
        return self.all()
    
    def create_rack(self, id_pedido):
        return self.create(id_pedido = id_pedido)

    def update_rack(self, rack_id, **kwargs):
        rack = self.get_by_id(rack_id)
        
        for key, value in kwargs.items():
            setattr(rack, key, value)
        
        rack.save()
        return rack
    
    def delete_rack(self, rack_id): 
        rack = self.get_by_id(rack_id)
        rack.delete()
        
        return rack

# Create your models here.
class Rack(models.Model):
    # TODO: make migrations of this model when table 'Pedido' is ready
    # id_pedido = models.ForeignKey('Pedido', on_delete = models.SET_NULL, null = True)
    id_pedido = models.BigIntegerField()
    
    objects = RackManager()