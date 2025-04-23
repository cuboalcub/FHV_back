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
        try:
            user = self.repository.get_user_by_username(data['username'])
            if user:
                if user.check_password(data['password']):
                    return {"token":JWTService.generate_token(user.id), "status": Responses.OK.value , "userType": user.is_superuser}
                else:
                    return {"status": Responses.UNAUTHORIZED.value}
        except User.DoesNotExist:
            return {"status": Responses.UNAUTHORIZED.value}
        except Exception as e:
            return {"status": Responses.INTERNAL_SERVER_ERROR.value, "error": str(e)}
