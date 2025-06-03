from django.forms import model_to_dict
from django.http import JsonResponse
from middlewares import jwt_required
from log_notificaciones.log_Service import LogService
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from JWTservice import JWTService
import json

service = LogService()
jwt = JWTService()


from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.forms.models import model_to_dict

@require_http_methods(["GET"])
def list(request, id):
    noti = service.get_notifications(group_id=id)
    if noti:
        noti = noti.order_by('-fecha')[:10]  # ordena por fecha descendente y limita a 10
        noti_list = [model_to_dict(n) for n in noti]
        return JsonResponse({"status": "success", "data": noti_list}, status=200)
    else:
        return JsonResponse({"status": "error", "message": "No notifications found"}, status=404)
