from django.urls import path, include 
from rest_framework.routers import DefaultRouter
from .views import RackViewSet

router = DefaultRouter()
router.register(r'racks', RackViewSet, basename = 'rack')

urlpatterns = [
    path('', include(router.urls)),
]