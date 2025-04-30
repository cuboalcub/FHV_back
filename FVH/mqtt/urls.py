
from django.urls import path
from mqtt.views import list
urlpatterns = [
    path('', list),

]