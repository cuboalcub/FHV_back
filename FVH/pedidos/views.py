from django.forms import model_to_dict
from django.http import JsonResponse
from django.contrib.auth.models import User
from middlewares import jwt_required
from pedidos.Pedidos_Service import PedidosService
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from pedidos.models import DetallePedido, Pedidos
from user.user_Service import UserService
import json

service = PedidosService()
userService = UserService()

@csrf_exempt
@jwt_required
@require_http_methods(["POST"])  
def list(request):
    id = json.loads(request.body)
    id = id.get("id")
    print(id)
    if id == "undefined" or id == None: 
        return JsonResponse({"status": 400, "message": "No se ha proporcionado un id"})
    pedidos = service.get_all(id)
    if len(pedidos["data"]) == 0:
        return JsonResponse({"status": 200, "message": "No hay pedidos"})
    pedidos = pedidos["data"]
    pedidos = [model_to_dict(pedido) for pedido in pedidos]

    for pedido in pedidos:
        detalle_pedido = DetallePedido.objects.filter(pedido_id=pedido["id"])
        detalle_pedido_list = []
        for detalle in detalle_pedido:
            detalle_dict = model_to_dict(detalle)
            detalle_pedido_list.append(detalle_dict)
        pedido["detalle_pedido"] = detalle_pedido_list

    return JsonResponse(pedidos, safe=False)

@jwt_required
@csrf_exempt
@require_http_methods(["POST"])
def create(request):        
    user_id = request.user_id
    data = json.loads(request.body)
    print(data)
    user_id = userService.get_by_id(user_id).get("data")
    data["user_id"] = user_id
    pedido = service.add(data).get("data") 
    print(pedido)
    return JsonResponse({'status': 201})

@jwt_required
@csrf_exempt
@require_http_methods(["PUT"])
def update_pedido(request, id):
        data = json.loads(request.body)
        user = userService.get_by_id(request.user_id).get("data")
        user = User(user)
        data["user_id"] = user
        response = service.update(id, data)
        return JsonResponse(response)


@jwt_required
@require_http_methods(["DELETE"])
@csrf_exempt
def delete_pedido(request, id):
    pedido = Pedidos.objects.filter(id=id).first()
    if not pedido:
        return JsonResponse({"message": "Pedido no encontrado"}, status=404)
    pedido.delete()
    return JsonResponse({"message": "Pedido eliminado exitosamente"}, status=200)

@csrf_exempt
@require_http_methods(["PATCH"])
def update_detalle(request):
    data = json.loads(request.body)
    print(data, "detalle")
    for id,detallepedido in data.items(): 
        detalle = DetallePedido.objects.filter(id=id).first()
        print(detalle, type(detalle), "detalle")
        pedido = Pedidos.objects.filter(id=model_to_dict(detalle).get("pedido_id")).first()
        pedido.estado = "En progreso"
        pedido.save()
        detalle.cantidad = detalle.cantidad - int(detallepedido)
        detalle.save()
    return JsonResponse({"message": "Pedido actualizado exitosamente"}, status=200)