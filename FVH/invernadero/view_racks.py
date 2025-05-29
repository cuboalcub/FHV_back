from django.http import JsonResponse
from middlewares import jwt_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from invernadero.Invernadero_Service import InvernaderoService
import json

service = InvernaderoService()

@jwt_required
@csrf_exempt
@require_http_methods(["GET"])
def list(request, id):
    response = service.get_all_racks(id)
    return JsonResponse(response, safe=False)

@jwt_required
@csrf_exempt
@require_http_methods(["POST"])
def create(request):
    data = json.loads(request.body)
    response = service.create_rack(data)
    return JsonResponse(response, safe=False)