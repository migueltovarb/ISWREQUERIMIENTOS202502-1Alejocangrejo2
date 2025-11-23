from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Notificacion, CorreoSimulado
from .serializers import NotificacionSerializer, CorreoSimuladoSerializer

class NotificacionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para notificaciones del usuario
    Solo lectura - las notificaciones se crean automáticamente por el sistema
    """
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Solo mostrar notificaciones del usuario logueado"""
        return self.request.user.notificaciones.all()
    
    @action(detail=True, methods=['post'])
    def marcar_leida(self, request, pk=None):
        """Marcar una notificación como leída"""
        notificacion = self.get_object()
        notificacion.marcar_leida()
        return Response({'status': 'Notificación marcada como leída'})
    
    @action(detail=False, methods=['post'])
    def marcar_todas_leidas(self, request):
        """Marcar todas las notificaciones como leídas"""
        request.user.notificaciones.filter(leida=False).update(leida=True)
        return Response({'status': 'Todas las notificaciones marcadas como leídas'})
    
    @action(detail=False, methods=['get'])
    def no_leidas(self, request):
        """Obtener cantidad de notificaciones no leídas"""
        count = request.user.notificaciones.filter(leida=False).count()
        return Response({'count': count})


class CorreoSimuladoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para correos simulados
    Solo para administradores
    """
    queryset = CorreoSimulado.objects.all()
    serializer_class = CorreoSimuladoSerializer
    permission_classes = [IsAdminUser]
    
    @action(detail=True, methods=['post'])
    def reintentar(self, request, pk=None):
        """Reintentar envío de un correo"""
        correo = self.get_object()
        correo.reintentar_envio()
        return Response({
            'status': 'Reintento exitoso',
            'intentos': correo.intentos
        })
