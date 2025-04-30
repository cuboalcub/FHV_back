from IService import IService
from log_Repository import LogRepository
from log_notificaciones.models import Notificacion
class LogService(IService):
    model = Notificacion
    repository = LogRepository()
    
    def __init__(self):
        super().__init__(model=self.model, repository=self.repository)