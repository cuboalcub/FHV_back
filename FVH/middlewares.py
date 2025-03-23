from django.http import JsonResponse
from functools import wraps
from JWTservice import JWTService  

def jwt_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("JWT "):
            return JsonResponse({"error": "Token missing or invalid"}, status=401)

        token = auth_header.split(" ")[1]
        payload = JWTService.decode_token(token)
        if not payload:
            return JsonResponse({"error": "Invalid or expired token"}, status=401)

        request.user_id = payload["user_id"]  # Guarda el user_id en el request
        return view_func(request, *args, **kwargs)
    
    return wrapper
