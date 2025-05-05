from typing import override
from ENUM_RESPONSES import Responses
from IRepository import BaseRepository
from invernadero.models import Invernadero, Racks, Bandeja

class InvernaderoRepository(BaseRepository):
    def __init__(self): 
        super().__init__(Invernadero)