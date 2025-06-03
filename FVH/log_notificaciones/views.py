from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from log_notificaciones.log_Service import LogService
from JWTservice import JWTService
from django.utils.dateformat import format as format_date

service = LogService()
jwt = JWTService()

@require_http_methods(["GET"])
def list(request, id):
    noti = service.get_notifications(group_id=id)
    if noti:
        noti = noti.order_by('-fecha')[:10]  # ordena por fecha descendente y limita a 10

        noti_list = []
        for n in noti:
            item = model_to_dict(n)
            item["fecha"] = format_date(n.fecha, 'c') if n.fecha else None  # ISO 8601
            noti_list.append(item)

        return JsonResponse({"status": "success", "data": noti_list}, status=200)
    else:
        return JsonResponse({"status": "error", "message": "No notifications found"}, status=404)
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from log_notificaciones.log_Service import LogService
from JWTservice import JWTService
from django.utils.dateformat import format as format_date

service = LogService()
jwt = JWTService()

@require_http_methods(["GET"])
def list(request, id):
    noti = service.get_notifications(group_id=id)
    if noti:
        noti = noti.order_by('-fecha')[:10]  # ordena por fecha descendente y limita a 10

        noti_list = []
        for n in noti:
            item = model_to_dict(n)
            item["fecha"] = format_date(n.fecha, 'c') if n.fecha else None  # ISO 8601
            noti_list.append(item)

        return JsonResponse({"status": "success", "data": noti_list}, status=200)
    else:
        return JsonResponse({"status": "error", "message": "No notifications found"}, status=404)
