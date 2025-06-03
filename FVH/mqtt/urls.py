
from django.urls import path
from mqtt.views import list, create, get_topics_sensores,get_topic_actuadores, mode_and_status, get_temperature
urlpatterns = [
    path('', list),
    path('create', create),
    path('get_topic_s/<int:id>', get_topics_sensores),
    path('get_topic_a/<int:id>', get_topic_actuadores),
    path('mode',mode_and_status ),
    path('get_temperature/<int:id>', get_temperature),
    
]