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
    try:
        # Obtén el group_id del usuario (ajusta según tu modelo User-Group)
        user = userService.get_by_id(request.user_id).get("data")
        group_id = user.group.id  # Asume que User tiene relación con Group
        
        response = service.get_all(group_id)  # Pasa el group_id, no el user_id
        return JsonResponse(response, safe=False)
    except Exception as e:
        return JsonResponse({"status": 500, "error": str(e)})

@csrf_exempt
@jwt_required
@require_http_methods(["POST"])
def create(request):
    user = userService.get_by_id(request.user_id).get("data")
    data = json.loads(request.body)
    response = service.create(data)
    return JsonResponse(response, safe=False)

@csrf_exempt
@jwt_required
@require_http_methods(["PUT"])
def update_pedido(request, id):
    data = json.loads(request.body)
    user = userService.get_by_id(request.user_id).get("data")
    data["user_id"] = user
    response = service.update(id, data)
    return JsonResponse(response)