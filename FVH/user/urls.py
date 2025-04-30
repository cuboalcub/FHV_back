from django.urls import path
from user.views import list, create_user, login
urlpatterns = [
    path('', list),
    path('singup', create_user),
    path('login', login),

]