from django.urls import path
from invernadero import views,view_racks,view_bandejas


urlpatterns = [
    path('', views.list, name='list'),
    path('create/', views.create, name='create'),
    path('racks/<int:id>', view_racks.list, name='racks_list'),
    path('racks/create/', view_racks.create, name='racks_create'),
    path('bandejas/<int:id>', view_bandejas.list, name='bandejas_list'),
    path('bandejas/create/', view_bandejas.create, name='bandejas_create'),
]