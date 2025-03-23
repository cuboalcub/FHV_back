from django.contrib.auth.models import User
from IRepository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

