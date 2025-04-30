from django.urls import path
from pedidos.views import list,create,update_pedido
urlpatterns = [
    path('', list),
    path('create', create ),
    path('put/<int:id>', update_pedido),

]