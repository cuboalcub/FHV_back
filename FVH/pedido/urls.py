from django.urls import path
from pedido.views import list
urlpatterns = [
    path('', list)

]