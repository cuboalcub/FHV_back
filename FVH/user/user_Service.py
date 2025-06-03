from typing import override
import traceback
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
        user = User.objects.create_user(username=data["username"], password=data['password'], email=data['email'])
        if user:
            return {"status": Responses.CREATED.value, "data": model_to_dict(user)}
        else:
            return {"status": Responses.BAD_REQUEST.value}

    def login(self, data):
        try:
            user = self.repository.get_user_by_username(data['username'])
            if user is None:
                return {"status": Responses.UNAUTHORIZED.value, "error": "Invalid username or password."}

            if not user.check_password(data['password']):
                return {"status": Responses.UNAUTHORIZED.value, "error": "Invalid username or password."}

            group = self.repository.user_in_group_by_id(user.id)

            response = {
                "token": JWTService.generate_token(user.id),
                "status": Responses.OK.value,
                "userType": user.is_superuser
            }

            if group:
                response["group"] = group

            return response
        except User.DoesNotExist:
            return {"status": Responses.UNAUTHORIZED.value, "error": "User does not exist"}
        except Exception as e:
            return {"status": Responses.INTERNAL_SERVER_ERROR.value, "error": str(e)}
        
    def create_group(self, data):
        try:
            # Validación básica de entrada
            group_name = data
            username = data

            
            group = self.repository.get_by_name(name=group_name)
            if isinstance(group, User):
                return {"status": Responses.BAD_REQUEST.value, "error": "Group already exists"}

            # Verifica si el usuario ya está en ese grupo
            user_in_group = self.repository.user_in_group(username=username)
            if user_in_group:
                return {"status": Responses.BAD_REQUEST.value, "error": "User already in group"}

            # Crea el grupo
            group = self.repository.create_group(name=group_name)
            if group:
                return {"status": Responses.CREATED.value, "data": model_to_dict(group)}
            else:
                return {"status": Responses.BAD_REQUEST.value, "error": "Group creation failed"}

        except Exception as e:
            return {
                "status": Responses.INTERNAL_SERVER_ERROR.value,
                "error": str(e),
                "trace": traceback.format_exc()
            }


    def add_user_group(self, data, user_admin):
        try:
            user_admin = model_to_dict(user_admin)
            user = self.repository.get_user_by_username(data['username'])
            if not user:
                return {"status": Responses.NOT_FOUND.value, "message": "User not found"}
                
            group = self.repository.get_by_name(user_admin.get("username"))
            if not group:
                return {"status": Responses.NOT_FOUND.value, "message": "Group not found"}
                
            detalle_group = self.repository.add_user_to_group(data['username'], data['email'], data["role"], group)
            
            if detalle_group:
                return {"status": Responses.CREATED.value, "data": model_to_dict(detalle_group)}
            return {"status": Responses.BAD_REQUEST.value, "message": "Failed to add user to group"}
            
        except Exception as e:
            return {
                "status": Responses.INTERNAL_SERVER_ERROR.value,
                "error": str(e),
                "trace": traceback.format_exc()
            }
        
    def get_group(self, user):
        try:
            detalle = self.repository.get_group(user)
            return {"status": Responses.OK.value, "data": detalle}
        except Exception as e:
            return {"status": Responses.INTERNAL_SERVER_ERROR.value, "error": str(e)}

    def delete_user(self, id):
        try:
            user = self.repository.delete_of_group(id)
            if not user:
                return {"status": Responses.NOT_FOUND.value, "error": "User not found"}
                
            user.delete()
            return {"status": Responses.OK.value, "message": "User deleted successfully"}
        except Exception as e:
            return {"status": Responses.INTERNAL_SERVER_ERROR.value, "error": str(e)}
        
    def update_user(self, id, data):
        try:
            user = self.repository.update_user(id,data)
            if not user:
                return {"status": Responses.NOT_FOUND.value, "error": "User not found"}
                
            user.save()
            return {"status": Responses.OK.value, "message": "User updated successfully"}
        except Exception as e:
            return {"status": Responses.INTERNAL_SERVER_ERROR.value, "error": str(e)}

