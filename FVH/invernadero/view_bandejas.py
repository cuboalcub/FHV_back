from django.http import JsonResponse
from middlewares import jwt_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from invernadero.Invernadero_Service import InvernaderoService
from user.user_Service import UserService
import json
from pedidos.Pedidos_Service import PedidosService
from invernadero.models import Bandeja

service = InvernaderoService()
userService = UserService()
pedidosService = PedidosService()

@jwt_required
@csrf_exempt
@require_http_methods(["GET"])
def list(request, id):
    response = service.get_all_bandejas(id)
    return JsonResponse(response, safe=False)

@jwt_required
@csrf_exempt
@require_http_methods(["POST"])
def create(request):
    data = json.loads(request.body)
    response = service.create_bandeja(data)
    return JsonResponse(response, safe=False)

@jwt_required
@csrf_exempt
@require_http_methods(["PATCH"])
def patch_peso_semilla(request):
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    pedido_id = data.get("pedido_id")
    if not pedido_id:
        return JsonResponse({'error': 'Falta pedido_id'}, status=400)

    pedido = pedidosService.get_by_id(pedido_id).get("data")
    if not pedido:
        return JsonResponse({'error': f'Pedido con id {pedido_id} no encontrado'}, status=404)

    # Actualiza sólo los campos permitidos para evitar problemas
    update_data = {}
    if "peso" in data:
        update_data["peso"] = data["peso"]
    if "semilla" in data:
        update_data["semilla"] = data["semilla"]

    if not update_data:
        return JsonResponse({'error': 'No hay datos para actualizar'}, status=400)

    try:
        Bandeja.objects.filter(id=data.get("id")).update(**update_data)
        return JsonResponse({"status": "actualizado"}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)