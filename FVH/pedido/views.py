from django.http import JsonResponse
from ENUM_RESPONSES import Responses
from middlewares import jwt_required
from pedido.pedido_Service import PedidoService
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json

service = PedidoService()

@jwt_required
@csrf_exempt
@require_http_methods(["GET"])
def list(request):
    data = json.loads(request.body)
    print(data)
    pedidos = service.get_all(data['user_id'])
    return JsonResponse(pedidos, safe=False)  # Devuelve JSON directamente


@jwt_required
@csrf_exempt
@require_http_methods(["POST"])
def create(request):
    data = json.loads(request.body)
    pedido = service.add(data)
    return JsonResponse(pedido, safe=False)  # Devuelve JSON directamente