from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'rol', 'telefono', 'is_active', 'is_staff']
    list_filter = ['rol', 'is_staff', 'is_active']
    search_fields = ['username', 'email']
    
    fieldsets = (
        ('Información de Usuario', {
            'fields': ('username', 'email', 'password')
        }),
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'telefono')
        }),
        ('Permisos', {
            'fields': ('rol', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Fechas Importantes', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo usuario
            if 'password' in form.cleaned_data:
                obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)
