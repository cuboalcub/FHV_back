from django.forms import model_to_dict
from django.http import JsonResponse
from middlewares import jwt_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from invernadero.Invernadero_Service import InvernaderoService
from user.user_Service import UserService
import json

service = InvernaderoService()
userService = UserService()


@jwt_required
@require_http_methods(["GET"])
def list(request):
    user = userService.get_by_id(request.user_id).get("data")
    invernaderos = service.get_all(user)
    return JsonResponse(invernaderos, safe=False)

@jwt_required
@csrf_exempt
@require_http_methods(["POST"])
def create(request):
    user = userService.get_by_id(request.user_id).get("data")
    data = json.loads(request.body)
    invernadero = service.create(data)
    return JsonResponse(invernadero, safe=False)


@jwt_required
@csrf_exempt
@require_http_methods(["PUT"])
def update_pedido(request, id):
        data = json.loads(request.body)
        user = userService.get_by_id(request.user_id).get("data")
        data["user_id"] = user
        response = service.update(id, data)
        return JsonResponse(response)


# @jwt_required
# @require_http_methods(["DELETE"])
# @csrf_exempt
# def delete_pedido(request, id):
#     user = userService.get_by_id(request.user_id).get("data")
#     pedido = Pedidos.objects.filter(id=id, user_id=user).first()
#     if not pedido:
#         return JsonResponse({"message": "Pedido no encontrado"}, status=404)
#     pedido.delete()
#     return JsonResponse({"message": "Pedido eliminado exitosamente"}, status=200)

