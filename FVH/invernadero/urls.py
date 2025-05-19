from django.urls import path
from invernadero import views,view_racks,view_bandejas


urlpatterns = [
    path('', views.list, ),
    path('create/', views.create, ),
    path('racks/<int:id>', view_racks.list, ),
    path('racks/create/', view_racks.create, ),
    path('bandejas/<int:id>', view_bandejas.list, ),
    path('bandejas/create/', view_bandejas.create, ),
    path('bandejas/peso_semilla', view_bandejas.patch_peso_semilla),
]