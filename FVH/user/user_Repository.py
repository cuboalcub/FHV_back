from typing import override
from django.contrib.auth.models import User
from IRepository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_username(self, username):
        try:
            user = self.model.objects.get(username=username)
            return user
        except self.model.DoesNotExist:
            return None
        
    @override
    def find_by_id(self, id):
        try:
            user = User.objects.get(id=id)    
            return user
        except self.model.DoesNotExist:
            return None
        
        
