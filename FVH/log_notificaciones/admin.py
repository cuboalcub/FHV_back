from django.contrib import admin
from .models import Notificacion

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario_id', 'mensaje', 'fecha')
    list_filter = ('fecha',)                                 
    search_fields = ('mensaje',)
