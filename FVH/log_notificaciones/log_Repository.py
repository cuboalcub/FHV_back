from IRepository import BaseRepository
from log_notificaciones.models import Notificacion


class LogRepository(BaseRepository):
    def __init__(self):
        super().__init__(Notificacion)
        