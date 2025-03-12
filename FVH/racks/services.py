from .models import Rack

class RackService:
    @staticmethod
    def get_rack_by_id(rack_id):
        return Rack.objects.get_by_id(rack_id)
    
    @staticmethod 
    def get_all_racks():
        return Rack.objects.get_all()
    
    @staticmethod
    def create_rack(id_pedido):
        return Rack.objects.create_rack(id_pedido = id_pedido)
    
    @staticmethod 
    def update_rack(rack_id, **data):
        return Rack.objects.update_rack(rack_id, **data)
    
    @staticmethod 
    def delete_rack(rack_id):
        return Rack.objects.delete_rack(rack_id)
    
    @staticmethod 
    def get_seed_by_rack(rack_id):
        return Rack.objects.get_seed_by_rack(rack_id)
