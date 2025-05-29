from django.urls import path
from user.views import (
    list_users,          # Antes era 'list'
    create_user,
    login,
    validate_token,
    create_group,
    add_user_group,
    get_group,
    delete_user_group,
    update_user_group
)

urlpatterns = [
    path('', list_users),  # No se cambia la ruta, solo el nombre interno
    path('singup', create_user),
    path('login', login),
    path('create_group', create_group),
    path('add_user_group', add_user_group),
    path('get_group', get_group),
    path('delete_user_group/<int:id>', delete_user_group),
    path('update_user/<int:id>', update_user_group),
    path('validate_token', validate_token),
]