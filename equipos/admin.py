from django.contrib import admin
from .models import Equipo, Laboratorio, Mantenimiento

@admin.register(Laboratorio)
class LaboratorioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'aforo_maximo', 'hora_apertura', 'hora_cierre']
    search_fields = ['nombre']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre',)
        }),
        ('Capacidad y Horarios', {
            'fields': ('aforo_maximo', 'hora_apertura', 'hora_cierre')
        }),
    )


@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'laboratorio', 'estado']
    list_filter = ['estado', 'laboratorio']
    search_fields = ['codigo']
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('codigo', 'laboratorio')
        }),
        ('Estado', {
            'fields': ('estado',)
        }),
    )


@admin.register(Mantenimiento)
class MantenimientoAdmin(admin.ModelAdmin):
    list_display = ['equipo', 'fecha_inicio', 'fecha_fin', 'activo']
    list_filter = ['activo', 'fecha_inicio']
    search_fields = ['equipo__codigo', 'motivo']
    date_hierarchy = 'fecha_inicio'
    
    fieldsets = (
        ('Información del Mantenimiento', {
            'fields': ('equipo', 'motivo')
        }),
        ('Programación', {
            'fields': ('fecha_inicio', 'fecha_fin')
        }),
        ('Estado', {
            'fields': ('activo',)
        }),
    )
