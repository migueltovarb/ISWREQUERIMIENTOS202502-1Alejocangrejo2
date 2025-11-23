from django.contrib import admin
from .models import Reserva

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['id', 'usuario', 'equipo', 'fecha_inicio', 'fecha_fin', 'estado']
    list_filter = ['estado', 'fecha_inicio']
    search_fields = ['usuario__username', 'equipo__codigo']
    date_hierarchy = 'fecha_inicio'
    
    fieldsets = (
        ('Información de Reserva', {
            'fields': ('usuario', 'equipo')
        }),
        ('Fechas y Horarios', {
            'fields': ('fecha_inicio', 'fecha_fin')
        }),
        ('Estado', {
            'fields': ('estado',)
        }),
    )
    
    actions = ['marcar_como_completada', 'cancelar_reservas']
    
    def marcar_como_completada(self, request, queryset):
        updated = queryset.update(estado='COMPLETADA')
        self.message_user(request, f'{updated} reserva(s) marcada(s) como completada(s).')
    marcar_como_completada.short_description = "Marcar como completada"
    
    def cancelar_reservas(self, request, queryset):
        updated = queryset.update(estado='CANCELADA')
        self.message_user(request, f'{updated} reserva(s) cancelada(s).')
    cancelar_reservas.short_description = "Cancelar reservas seleccionadas"
