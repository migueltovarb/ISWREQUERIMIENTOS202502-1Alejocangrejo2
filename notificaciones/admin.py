from django.contrib import admin
from .models import Notificacion, CorreoSimulado

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tipo', 'mensaje_corto', 'leida', 'created_at']
    list_filter = ['tipo', 'leida', 'created_at']
    search_fields = ['usuario__username', 'mensaje']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Destinatario', {
            'fields': ('usuario',)
        }),
        ('Contenido', {
            'fields': ('tipo', 'mensaje')
        }),
        ('Estado', {
            'fields': ('leida',)
        }),
    )
    
    def mensaje_corto(self, obj):
        return obj.mensaje[:50] + '...' if len(obj.mensaje) > 50 else obj.mensaje
    mensaje_corto.short_description = 'Mensaje'
    
    actions = ['marcar_como_leida']
    
    def marcar_como_leida(self, request, queryset):
        updated = queryset.update(leida=True)
        self.message_user(request, f'{updated} notificación(es) marcada(s) como leída(s).')
    marcar_como_leida.short_description = "Marcar como leída"


@admin.register(CorreoSimulado)
class CorreoSimuladoAdmin(admin.ModelAdmin):
    list_display = ['destinatario', 'asunto', 'estado', 'intentos', 'fecha_envio']
    list_filter = ['estado', 'created_at']
    search_fields = ['destinatario', 'asunto']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Destinatario y Asunto', {
            'fields': ('destinatario', 'asunto')
        }),
        ('Contenido', {
            'fields': ('cuerpo',)
        }),
        ('Estado de Envío', {
            'fields': ('estado', 'intentos', 'fecha_envio', 'error')
        }),
    )
    
    actions = ['reintentar_envio_action']
    
    def reintentar_envio_action(self, request, queryset):
        for correo in queryset:
            correo.reintentar_envio()
        self.message_user(request, f'Se reintentó el envío de {queryset.count()} correo(s).')
    reintentar_envio_action.short_description = "Reintentar envío"
