from rest_framework import serializers
from .models import Notificacion, CorreoSimulado

class NotificacionSerializer(serializers.ModelSerializer):
    """Serializer para notificaciones del usuario"""
    
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    fecha = serializers.DateTimeField(source='created_at', read_only=True)
    
    class Meta:
        model = Notificacion
        fields = ['id', 'tipo', 'tipo_display', 'mensaje', 'leida', 'fecha']
        read_only_fields = ['id', 'tipo', 'mensaje', 'fecha']


class CorreoSimuladoSerializer(serializers.ModelSerializer):
    """Serializer para correos simulados (solo admin)"""
    
    estado_display = serializers.CharField(source='get_estado_display', read_only=True)
    
    class Meta:
        model = CorreoSimulado
        fields = [
            'id', 'destinatario', 'asunto', 'cuerpo', 
            'estado', 'estado_display', 'intentos', 
            'fecha_envio', 'error', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

