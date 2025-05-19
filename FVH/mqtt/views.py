import json
import threading
import paho.mqtt.client as mqtt
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from log_notificaciones.log_Service import LogService
from django.contrib.auth.models import User
from mqtt.models import Mqtt

log_service = LogService()
service = UserService()

MQTT_BROKER_HOST = settings.MQTT_BROKER_HOST
MQTT_BROKER_PORT = settings.MQTT_BROKER_PORT
MQTT_TOPIC = "greenhouse/greenhouse-2/actuator/notification"

# Función llamada cuando se recibe un mensaje del broker
def on_message(client, userdata, message):
    try:
        mensaje = message.payload.decode()  # Asumimos que llega como texto plano

        # Obtenemos todos los usuarios que no son administradores
        usuarios = User.objects.filter(is_superuser=False)

        # Guardamos una notificación para cada usuario
        for usuario in usuarios:
            log_service.create({
                'usuario_id': usuario,  # Aquí pasamos la instancia completa de User
                'mensaje': mensaje
            })
        
        print(f"Mensaje guardado para {usuarios.count()} usuarios comunes: {mensaje}")
    except Exception as e:
        print(f"Error al procesar el mensaje: {e}")

# Función para iniciar el cliente MQTT en segundo plano
def iniciar_cliente_mqtt():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
    client.subscribe(MQTT_TOPIC)
    client.loop_forever()

# Iniciar el cliente MQTT en un hilo para no bloquear Django
mqtt_thread = threading.Thread(target=iniciar_cliente_mqtt)
mqtt_thread.daemon = True
mqtt_thread.start()



@csrf_exempt
@require_http_methods(["POST"])
def list(request):
    data = json.loads(request.body)
    print(data)
    return JsonResponse({"error": "Method not allowed"}, status=200)
    payload = data.get("payload")
    payload = json.loads(payload) if isinstance(payload, str) else payload
    data["payload"] = payload.get("value")
    print(data)
    
    Mqtt.objects.create(
        topic=data["topic"],
        payload=data["payload"],
        qos=data["qos"]
    )
    return JsonResponse({"error": "Method not allowed"}, status=200)
