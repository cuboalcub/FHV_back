from django.http import JsonResponse
from middlewares import jwt_required
from user.user_Service import UserService
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
service = UserService()


@jwt_required
@require_http_methods(["GET"])
def list(request):
    users = service.get_all()
    return JsonResponse(users, safe=False)  

@csrf_exempt
@require_http_methods(["POST"])
def create_user(request):
    data = json.loads(request.body)
    user = service.add(data)
    return JsonResponse(user, safe=False)  

@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    data = json.loads(request.body)
    print(data)
    user = service.login(data)
    print(user)
    return JsonResponse(user, safe=False)  