from django.urls import path
from user.views import list, create_user, login
urlpatterns = [
    path('', list),
    path('create_user', create_user),
    path('login', login),

]