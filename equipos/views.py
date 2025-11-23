from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils import timezone
from .models import Equipo, Laboratorio, Mantenimiento
from .serializers import EquipoSerializer, LaboratorioSerializer, MantenimientoSerializer
from .services import bloquear_equipo, desbloquear_equipo

class LaboratorioViewSet(viewsets.ModelViewSet):
    """ViewSet para laboratorios (solo lectura para estudiantes, edición para admins)"""
    queryset = Laboratorio.objects.all()
    serializer_class = LaboratorioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """Solo admins pueden crear/modificar/eliminar"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def modificar_aforo(self, request, pk=None):
        """Modificar el aforo máximo del laboratorio"""
        laboratorio = self.get_object()
        nuevo_aforo = request.data.get('aforo_maximo')
        
        if not nuevo_aforo or int(nuevo_aforo) < 1:
            return Response(
                {'error': 'Aforo inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        aforo_anterior = laboratorio.aforo_maximo
        laboratorio.aforo_maximo = int(nuevo_aforo)
        laboratorio.save()
        
        # Notificar a administradores
        from notificaciones.services import notificar_aforo_modificado
        notificar_aforo_modificado(laboratorio, nuevo_aforo, request.user)
        
        return Response({
            'status': 'Aforo modificado',
            'aforo_anterior': aforo_anterior,
            'aforo_nuevo': nuevo_aforo
        })


class EquipoViewSet(viewsets.ModelViewSet):
    """ViewSet para equipos"""
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        """Solo admins pueden crear/modificar/eliminar"""
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'bloquear', 'desbloquear']:
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        """Filtrar por laboratorio si se especifica"""
        queryset = Equipo.objects.all()
        laboratorio_id = self.request.query_params.get('laboratorio', None)
        
        if laboratorio_id:
            queryset = queryset.filter(laboratorio_id=laboratorio_id)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def disponibles(self, request):
        """Obtener solo equipos disponibles"""
        equipos = Equipo.objects.filter(estado='DISPONIBLE')
        serializer = self.get_serializer(equipos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def bloquear(self, request, pk=None):
        """Bloquear equipo por mantenimiento"""
        equipo = self.get_object()
        
        fecha_inicio = request.data.get('fecha_inicio')
        fecha_fin = request.data.get('fecha_fin')
        motivo = request.data.get('motivo', 'Mantenimiento programado')
        
        if not fecha_inicio or not fecha_fin:
            return Response(
                {'error': 'Debe especificar fecha_inicio y fecha_fin'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            from django.utils.dateparse import parse_datetime
            fecha_inicio_dt = parse_datetime(fecha_inicio)
            fecha_fin_dt = parse_datetime(fecha_fin)
            
            # Usar el servicio de ejemplo
            mantenimiento = bloquear_equipo(
                equipo_id=equipo.id,
                fecha_inicio=fecha_inicio_dt,
                fecha_fin=fecha_fin_dt,
                motivo=motivo
            )
            
            return Response({
                'status': 'Equipo bloqueado',
                'mantenimiento_id': mantenimiento.id,
                'reservas_canceladas': 'Se han notificado las cancelaciones'
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def desbloquear(self, request, pk=None):
        """Desbloquear equipo (finalizar mantenimiento)"""
        equipo = self.get_object()
        
        try:
            equipo_desbloqueado = desbloquear_equipo(equipo.id)
            return Response({
                'status': 'Equipo desbloqueado',
                'equipo': self.get_serializer(equipo_desbloqueado).data
            })
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class MantenimientoViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet para historial de mantenimientos (solo lectura)"""
    queryset = Mantenimiento.objects.all()
    serializer_class = MantenimientoSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        """Filtrar por equipo si se especifica"""
        queryset = Mantenimiento.objects.all()
        equipo_id = self.request.query_params.get('equipo', None)
        
        if equipo_id:
            queryset = queryset.filter(equipo_id=equipo_id)
        
        return queryset
