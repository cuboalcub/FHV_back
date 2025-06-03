
from django.urls import path
from log_notificaciones.views import list
urlpatterns = [
    path('list/<int:id>', list)
]