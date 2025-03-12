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
    
    def get_seed_by_rack(self, rack_id):
        rack = self.get_by_id(rack_id)
        
        # Verificar si rack tiene pedido y si el pedido tiene una semilla
        if rack.id_pedido and rack.id_pedido.semilla:
            return rack.id_pedido.semilla.nombre  # Acceder al nombre de la semilla
    
        return None  # Si no tiene semilla, devolver None

# Create your models here.
class Rack(models.Model):
    # TODO: make migrations of this model when table 'Pedido' is ready
    # id_pedido = models.ForeignKey('Pedido', on_delete = models.SET_NULL, null = True)
    id_pedido = models.BigIntegerField()
    
    objects = RackManager()