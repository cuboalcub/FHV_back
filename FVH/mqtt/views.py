import json
import threading
from django.forms import model_to_dict
import paho.mqtt.client as mqtt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from middlewares import jwt_required
from invernadero.models import Invernadero
from log_notificaciones.log_Service import LogService
from user.user_Service import UserService
from django.contrib.auth.models import User
from mqtt.models import Mqtt
from user.models import Group

log_service = LogService()
service = UserService()

#se modificó esta parte porque entraba em loop infinito al cargar antes la base que intentar crearla
MQTT_BROKER_HOST = settings.MQTT_BROKER_HOST
MQTT_BROKER_PORT = settings.MQTT_BROKER_PORT    
def get_notificaciones():
    """Obtiene los tópicos de notificación dinámicamente."""
    topicos = Mqtt.objects.all()
    topicos_list = [topic.topic for topic in topicos]
    return [topic for topic in topicos_list if "/notification" in topic]

notificaciones = []

def on_message(client, userdata, message):
    try:
        mensaje = message.payload.decode()  # Asumimos que llega como texto plano
        topico = message.topic
        print(f"Mensaje recibido en el tópico {topico}: {mensaje}")
        grupos = [model_to_dict(topic.invernadero).get("group_id") for topic in topicos if topico == topic.topic]
        
        for g in grupos:
            grupo = Group.objects.filter(id=g).first()
            if grupo:
                log_service.create(
                    {
                        'group_id': grupo,  # Pasamos la instancia completa del Group
                        'mensaje': mensaje
                    }
                )
        
    except Exception as e:
        print(f"Error al procesar el mensaje: {e}")

# Función para iniciar el cliente MQTT en segundo plano
#Este igual se modificó
def iniciar_cliente_mqtt():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
    
    # Carga los tópicos solo cuando se llama la función (no al importar el módulo)
    notificaciones = get_notificaciones()  # ← Ahora se ejecuta después de las migraciones
    for notificacion in notificaciones:
        client.subscribe(notificacion)
    client.loop_forever()

# Iniciar el cliente MQTT en un hilo para no bloquear Django
mqtt_thread = threading.Thread(target=iniciar_cliente_mqtt)
mqtt_thread.daemon = True
mqtt_thread.start()

@csrf_exempt
@require_http_methods(["POST"])
def list(request):
    try:
        data = json.loads(request.body)
        print(data)
        
        payload = data.get("payload")
        payload = json.loads(payload) if isinstance(payload, str) else payload
        data["payload"] = payload.get("value")
        print(data)
        
        Mqtt.objects.create(
            topic=data["topic"],
            payload=data["payload"],
            qos=data["qos"]
        )
        return JsonResponse({"status": "success", "message": "MQTT data saved successfully"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def create(request):
    try:
        data = json.loads(request.body)
        invernadero = Invernadero.objects.get(id=data.get("invernadero"))
        data["invernadero"] = invernadero
        mqtt = Mqtt.objects.create(
            **data
        )
        return JsonResponse({"status": "success", "message": "MQTT data saved successfully", "id": mqtt.id}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
        
@csrf_exempt
@require_http_methods(["GET"])
def topic(request):
    try:
        # Obtener todos los tópicos de notificación con su información asociada
        topicos_notificacion = Mqtt.objects.filter(topic__contains="/notification")
        
        # Crear una lista con los datos relevantes
        resultado = []
        for topic in topicos_notificacion:
            if topic.invernadero:
                grupo_id = topic.invernadero.group_id
                resultado.append({
                    'topic': topic.topic,
                    'invernadero_id': topic.invernadero.id,
                    'group_id': grupo_id
                })
        
        return JsonResponse(resultado, safe=False)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@jwt_required
@require_http_methods(["GET"])
def get_topics_sensores(request,id):
    try:
        inv = Invernadero.objects.filter(id=id).first()
        topicos = Mqtt.objects.filter(invernadero = inv)
        topicos = [model_to_dict(topic).get("topic") for topic in topicos ]
        print(topicos)
        resultado = [topic for topic in topicos if  "/sensor" in topic]
        print(resultado)
        return JsonResponse(resultado, safe=False)
    except Exception as e:  
        return JsonResponse({"error": str(e)}, status=400)

@csrf_exempt
@require_http_methods(["GET"])
def get_topic_actuadores(s, id):
    try:
        inv = Invernadero.objects.filter(id=id).first()
        topicos = Mqtt.objects.filter(invernadero = inv)
        topicos = [model_to_dict(topic).get("topic") for topic in topicos ]
        print(topicos)
        resultado = [topic for topic in topicos if  "/actuator" in topic ]
        print(resultado)
        return JsonResponse(resultado, safe=False)
    except Exception as e:  
        return JsonResponse({"error": str(e)}, status=400)

# @csrf_exempt
# @jwt_required
# @require_http_methods(["POST"])
# def mode_and_status(request):
#     try:
#         data = json.loads(request.body)
#         invernadero = Invernadero.objects.get(id=data.get("invernadero"))
#         topic = Mqtt.objects.get(topic=data.get("topic"), invernadero=invernadero)
        
#         # Actualizar el payload con el nuevo valor
#         topic.payload = data.get("payload")
#         topic.save()
        
#         return JsonResponse({"status": "success", "message": "MQTT data updated successfully"}, status=200)
#     except Exception as e:
#         return JsonResponse({"error": str(e)}, status=400)






