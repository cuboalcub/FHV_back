from IService import IService
from .log_Repository import LogRepository
from log_notificaciones.models import Notificacion


class LogService(IService):
    model = Notificacion
    repository = LogRepository()
    
    def __init__(self):
        super().__init__(model=self.model, repository=self.repository)

    #Código nuevo:

    def create(self, data):
        """
        Crea una notificación en la base de datos.
        :param data: Diccionario con los datos de la notificación (group_id, mensaje)
        """
        try:
            # Crear y guardar la notificación
            notificacion = self.model.objects.create(
                group_id=data['group_id'], 
                mensaje=data['mensaje']
            )
            return notificacion
        except Exception as e:
            print(f"Error al crear la notificación: {e}")
            return None
        
    def get_notifications(self, group_id):
        """
        Obtiene todas las notificaciones asociadas a un group_id.
        :param group_id: ID del grupo al que pertenecen las notificaciones
        :return: Lista de notificaciones
        """
        try:
            notifications = self.model.objects.filter(group_id=group_id)
            return notifications
        except Exception as e:
            print(f"Error al obtener las notificaciones: {e}")
            return []