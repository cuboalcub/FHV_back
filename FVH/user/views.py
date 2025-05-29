from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from middlewares import jwt_required
from JWTservice import JWTService
from .models import Group, detalleGroup
from .serializer import UserSerializer, GroupSerializer, DetalleGroupSerializer
from user.user_Service import UserService

import json

service = UserService()
jwt = JWTService()

# User Endpoints
@require_http_methods(["GET"])
def list_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def create_user(request):
    try:
        data = json.loads(request.body)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            if data.get('is_superuser', False):
                User.objects.create_superuser(
                    username=data['username'],
                    email=data.get('email', ''),
                    password=data['password']
                )
            else:
                serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def login(request):
    data = json.loads(request.body)
    user = service.login(data)
    return JsonResponse(user, safe=False)

# Group Endpoints
@csrf_exempt
@jwt_required
@require_http_methods(["POST"])
def create_group(request):
    data = json.loads(request.body)
    serializer = GroupSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)

@jwt_required
@require_http_methods(["GET"])
def get_group(request):
    groups = Group.objects.all()
    serializer = GroupSerializer(groups, many=True)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
@jwt_required
@require_http_methods(["POST"])
def add_user_group(request):
    data = json.loads(request.body)
    serializer = DetalleGroupSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=201)
    return JsonResponse(serializer.errors, status=400)

@csrf_exempt
@jwt_required
@require_http_methods(["DELETE"])
def delete_user_group(request, id):
    try:
        detalle = detalleGroup.objects.get(id=id)
        detalle.delete()
        return JsonResponse({'status': 'deleted'}, status=200)
    except detalleGroup.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

@csrf_exempt
@jwt_required
@require_http_methods(["PUT"])
def update_user_group(request, id):
    try:
        detalle = detalleGroup.objects.get(id=id)
        serializer = DetalleGroupSerializer(detalle, data=json.loads(request.body), partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    except detalleGroup.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=404)

# Auth Endpoints
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