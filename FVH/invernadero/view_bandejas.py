from django.forms import model_to_dict
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
def list(request,id):
    racks = service.get_all_bandejas(id)
    return JsonResponse(racks, safe=False)

@jwt_required
@csrf_exempt
@require_http_methods(["POST"])
def create(request):
    data  = json.loads(request.body)
    rack = service.create_bandeja(data) 
    return JsonResponse(rack, safe=False)

@jwt_required
@csrf_exempt
@require_http_methods(["PATCH"])
def patch_peso_semilla(request):
    try:
            data = json.loads(request.body)  # Asegúrate de parsear el JSON
            print(data, type(data))
    except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)

    pedid = data.get("pedido_id")  # Usa .get para evitar KeyError
    if not pedid:
            return JsonResponse({'error': 'Falta pedido_id'}, status=400)

    pedido = pedidosService.get_by_id(pedid).get("data")
    if not pedido:
            return JsonResponse({'error': f'Pedido con id {pedid} no encontrado'}, status=404)

    data["pedido_id"] = pedido  # No es común reasignar aquí, pero depende de lo que sigue
    Bandeja.objects.filter(id=data["id"]).update(**data)
    return JsonResponse("saas", safe=False)






