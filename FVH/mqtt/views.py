import json
from django.http import JsonResponse
from user.user_Service import UserService
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

service = UserService()


@csrf_exempt
@require_http_methods(["POST"])
def list(request):
    data = json.loads(request.body)
    print(data)
    return JsonResponse({"error": "Method not allowed"}, status=200)
