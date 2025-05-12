import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from mqtt.models import Mqtt

@csrf_exempt
@require_http_methods(["POST"])
def list(request):
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
    return JsonResponse({"error": "Method not allowed"}, status=200)
