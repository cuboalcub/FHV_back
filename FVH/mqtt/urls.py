
from django.urls import path
from mqtt.views import list, create, get_topics_sensores,get_topic_actuadores
urlpatterns = [
    path('', list),
    path('create', create),
    path('get_topic_s/<int:id>', get_topics_sensores),
    path('get_topic_a/<int:id>', get_topic_actuadores),
    
]