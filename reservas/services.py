from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q
from .models import Reserva
from equipos.models import Equipo
from notificaciones.services import notificar_reserva_creada, notificar_reserva_cancelada

def crear_reserva(usuario, equipo, fecha_inicio, fecha_fin):
    """
    Función de ejemplo: Crear una reserva con todas las validaciones
    
    Args:
        usuario: Instancia de Usuario
        equipo: Instancia de Equipo (puede ser ID o instancia)
        fecha_inicio: datetime
        fecha_fin: datetime
    
    Returns:
        Reserva creada
    
    Raises:
        ValidationError: Si la reserva no es válida
    """
    # Obtener equipo si se pasó un ID
    if isinstance(equipo, int):
        try:
            equipo = Equipo.objects.get(pk=equipo)
        except Equipo.DoesNotExist:
            raise ValidationError('El equipo especificado no existe')
    
    # Crear la reserva
    reserva = Reserva(
        usuario=usuario,
        equipo=equipo,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        estado='ACTIVA'
    )
    
    # Ejecutar validaciones
    reserva.full_clean()
    
    # Guardar
    reserva.save()
    
    # Enviar notificaciones
    notificar_reserva_creada(reserva)
    
    return reserva


def cancelar_reserva(reserva_id, usuario):
    """
    Función de ejemplo: Cancelar una reserva
    
    Args:
        reserva_id: ID de la reserva
        usuario: Usuario que solicita la cancelación
    
    Returns:
        Reserva cancelada
    
    Raises:
        ValidationError: Si no se puede cancelar
    """
    try:
        reserva = Reserva.objects.get(pk=reserva_id)
    except Reserva.DoesNotExist:
        raise ValidationError('La reserva no existe')
    
    # Verificar permisos: solo el dueño o un admin pueden cancelar
    if reserva.usuario != usuario and usuario.rol != 'ADMIN':
        raise ValidationError('No tienes permiso para cancelar esta reserva')
    
    # Verificar estado
    if reserva.estado == 'CANCELADA':
        raise ValidationError('La reserva ya está cancelada')
    
    if reserva.estado == 'COMPLETADA':
        raise ValidationError('No se puede cancelar una reserva completada')
    
    # Cancelar
    reserva.cancelar()
    
    # Notificar
    notificar_reserva_cancelada(reserva)
    
    return reserva


def consultar_disponibilidad(fecha, laboratorio_id=None):
    """
    Función de ejemplo: Consultar disponibilidad para el calendario
    
    Args:
        fecha: datetime - Fecha para consultar
        laboratorio_id: ID del laboratorio (opcional)
    
    Returns:
        dict con información de disponibilidad por equipo
    """
    from equipos.models import Equipo
    
    # Filtrar equipos
    equipos_query = Equipo.objects.filter(estado='DISPONIBLE')
    if laboratorio_id:
        equipos_query = equipos_query.filter(laboratorio_id=laboratorio_id)
    
    disponibilidad = []
    
    for equipo in equipos_query:
        # Obtener reservas del día
        reservas_dia = Reserva.objects.filter(
            equipo=equipo,
            estado='ACTIVA',
            fecha_inicio__date=fecha.date()
        ).order_by('fecha_inicio')
        
        disponibilidad.append({
            'equipo_id': equipo.id,
            'equipo_codigo': equipo.codigo,
            'laboratorio': equipo.laboratorio.nombre,
            'reservas': [
                {
                    'inicio': reserva.fecha_inicio,
                    'fin': reserva.fecha_fin,
                    'usuario': reserva.usuario.username
                }
                for reserva in reservas_dia
            ]
        })
    
    return disponibilidad


def obtener_historial_usuario(usuario):
    """
    Obtener historial de reservas de un usuario
    
    Args:
        usuario: Instancia de Usuario
    
    Returns:
        QuerySet de reservas ordenadas por fecha
    """
    return usuario.reservas.all().order_by('-fecha_inicio')
