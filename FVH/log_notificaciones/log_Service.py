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
        :param data: Diccionario con los datos de la notificación (usuario_id, mensaje)
        """
        try:
            # Crear y guardar la notificación
            notificacion = self.model.objects.create(
                usuario_id=data['usuario_id'], 
                mensaje=data['mensaje']
            )
            return notificacion
        except Exception as e:
            print(f"Error al crear la notificación: {e}")
            return None