from typing import override
from .user_Repository import UserRepository
from .user_Validator import UserValidator
from django.contrib.auth.models import User
from IService import IService
from django.forms.models import model_to_dict
from ENUM_RESPONSES import Responses
from JWTservice import JWTService

class UserService(IService):
    model = User  
    repository = UserRepository()
    JWTService = JWTService()
    
    def __init__(self):
        super().__init__(model=self.model, repository=self.repository, )
    
    @override
    def add(self, data):
        user = User.objects.create_user(**data)
        if user:
            return {"status": Responses.CREATED.value, "data": model_to_dict(user)}
        else:
            return {"status": Responses.BAD_REQUEST.value}

    def login(self, data):
        user = User.objects.get(username=data['username'])
        if user:
            if user.check_password(data['password']):
                return JWTService.generate_token(user.id)
            else:
                return {"status": Responses.UNAUTHORIZED.value}
