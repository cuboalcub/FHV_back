import traceback
from typing import override
from django.contrib.auth.models import User
from django.forms import model_to_dict
from user.models import Group, detalleGroup

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


    def create_group(self, name):
        try:
            group = Group.objects.create(name=name)
            detalleGroup.objects.create(group_id=group, user_id= self.model.objects.get(username=name))
            return group
        except Exception as e:
            return None

    def add_user_to_group(self, username, email, role, group):
        try:
            # Verify if group is already a Group object or needs to be converted
            if not isinstance(group, Group):
                group_data = model_to_dict(group)
                group = Group.objects.get(name=group_data["name"])

            # Check if user exists
            user = User.objects.get(username=username, email=email)
            if role == "Admin":
                print("User is admin")
                user.is_superuser = True
                user.save()
            # Check if user is already in the group
            if detalleGroup.objects.filter(group_id=group, user_id=user).exists():
                print("User is already in the group")
                return None
                
            # Create the relationship
            detalle_group = detalleGroup.objects.create(group_id=group, user_id=user)
            
            print("User added to group successfully")
            return detalle_group
            
        except User.DoesNotExist:
            print("User not found")
            return None
        except Group.DoesNotExist:
            print("Group not found")
            return None
        except Exception as e:
            print(f"Unknown error: {str(e)}")
            return None




    def get_group(self, user_data):
        try:
            user_admin = self.model.objects.get(username=user_data["username"])
            detalle = detalleGroup.objects.filter(user_id=user_admin).first()
            if not detalle:
                return {"error": "User is not assigned to any group."}
            

            detalle_groups = detalleGroup.objects.filter(group_id=detalle.group_id.id)
            detalle_groups = [model_to_dict(detalle_group) for detalle_group in detalle_groups]
            detalle_groups = [detalle_group for detalle_group in detalle_groups if detalle_group["user_id"] != user_admin.id]
            users= []
            for detalle_group in detalle_groups:
                user = User.objects.get(id=detalle_group["user_id"])
                user = model_to_dict(user)   
                user_list= {k: v for k, v in user.items() if k in ["username", "email", "is_superuser"] }
                user_list["id"] = detalle_group["id"]
                users.append(user_list)
            return users
        except self.model.DoesNotExist:
            return {"status": 404, "error": "User not found"}
        except Exception as e:
            print(f"Error completo: {traceback.format_exc()}")  # Debug crítico
            return {"status": 500, "error": str(e)}

    def get_by_name(self, name):
        try:
            group = Group.objects.filter(name=name).first()
            return group
        except self.model.DoesNotExist:
            return None

    def user_in_group(self, username):
        try:
            user = User.objects.get(username=username)
            return detalleGroup.objects.filter(user_id=user).exists()
        except User.DoesNotExist:
            return False
        
    def delete_of_group(self, id):
        try:
            detalle = detalleGroup.objects.get(id=id)
            if not detalle:
                return None
            detalle.delete()
            return detalle
        except detalleGroup.DoesNotExist:
            return None
        except Exception as e:
            print(f"Error completo: {traceback.format_exc()}")

    def update_user(self, id, data):
        try:
            detalle = detalleGroup.objects.get(id=id)
            if not detalle:
                return None
            detalle.user_id.username = data["username"]
            detalle.user_id.email = data["email"]
            if data["role"] == "Admin":
                detalle.user_id.is_superuser = True
            else:
                detalle.user_id.is_superuser = False
            detalle.user_id.save()
        except detalleGroup.DoesNotExist:
            return None
        except Exception as e:
            print(f"Error completo: {traceback.format_exc()}")
