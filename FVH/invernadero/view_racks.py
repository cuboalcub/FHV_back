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
@csrf_exempt
@require_http_methods(["GET"])
def list(request,id):
    racks = service.get_all_racks(id)
    return JsonResponse(racks, safe=False)

@jwt_required
@csrf_exempt
@require_http_methods(["POST"])
def create(request):
    data  = json.loads(request.body)
    rack = service.create_rack(data)
    return JsonResponse(rack, safe=False)


