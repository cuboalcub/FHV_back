from django.forms import model_to_dict
from django.http import JsonResponse
from middlewares import jwt_required
from user.user_Service import UserService
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from JWTservice import JWTService
import json

service = UserService()
jwt = JWTService()


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
    user = service.login(data)
    return JsonResponse(user, safe=False)  


@csrf_exempt
@require_http_methods(["POST"])
def validate_token(request):
    token = json.loads(request.body).get("token")
    if not token:
        return JsonResponse({"error": "Token not provided"}, status=401)
    user_id = jwt.validate_token(token)
    if user_id.get("error"):
        return JsonResponse(user_id, status=401)
    return JsonResponse({"status": 200, "user_id": user_id})

@csrf_exempt
@jwt_required
@require_http_methods(["POST"])
def add_user_group(request):
    user = service.get_by_id(request.user_id).get("data")
    data = json.loads(request.body)
    user = service.add_user_group(data , user)
    return JsonResponse(user, safe=False)

@csrf_exempt
@jwt_required
@require_http_methods(["POST"])
def create_group(request):
    user = service.get_by_id(request.user_id).get("data")
    group = service.create_group(user.get("username"))
    return JsonResponse(group, safe=False)

@jwt_required
@require_http_methods(["GET"])
def get_group(request):
    user = service.get_by_id(request.user_id).get("data")
    group = service.get_group(user)
    return JsonResponse(group, safe=False)

@csrf_exempt
@jwt_required
@require_http_methods(["DELETE"])
def delete_user_group(request,id):
    group = service.delete_user(id)
    return JsonResponse(group, safe=False)

@csrf_exempt
@jwt_required
@require_http_methods(["PUT"])
def update_user_group(request,id):
    data = json.loads(request.body)
    group = service.update_user(data=data, id=id)
    return JsonResponse(group, safe=False)