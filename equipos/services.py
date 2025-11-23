from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Q
from .models import Equipo, Mantenimiento
from reservas.models import Reserva
from notificaciones.services import notificar_equipo_bloqueado

def bloquear_equipo(equipo_id, fecha_inicio, fecha_fin, motivo):
    """
    Función de ejemplo: Bloquear un equipo por mantenimiento
    
    Args:
        equipo_id: ID del equipo
        fecha_inicio: datetime de inicio del mantenimiento
        fecha_fin: datetime de fin del mantenimiento
        motivo: str - Razón del bloqueo
    
    Returns:
        Mantenimiento creado
    
    Raises:
        ValidationError: Si no se puede bloquear
    """
    try:
        equipo = Equipo.objects.get(pk=equipo_id)
    except Equipo.DoesNotExist:
        raise ValidationError('El equipo no existe')
    
    # Validar fechas
    if fecha_fin <= fecha_inicio:
        raise ValidationError('La fecha de fin debe ser posterior a la fecha de inicio')
    
    # Crear mantenimiento
    mantenimiento = Mantenimiento.objects.create(
        equipo=equipo,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
        motivo=motivo,
        activo=True
    )
    
    # Cambiar estado del equipo
    equipo.estado = 'MANTENIMIENTO'
    equipo.save()
    
    # Cancelar reservas afectadas
    reservas_afectadas = Reserva.objects.filter(
        equipo=equipo,
        estado='ACTIVA',
        fecha_inicio__lt=fecha_fin,
        fecha_fin__gt=fecha_inicio
    )
    
    for reserva in reservas_afectadas:
        reserva.estado = 'CANCELADA'
        reserva.save()
    
    # Notificar a usuarios afectados
    notificar_equipo_bloqueado(equipo, mantenimiento)
    
    return mantenimiento


def desbloquear_equipo(equipo_id):
    """
    Función de ejemplo: Desbloquear un equipo (finalizar mantenimiento)
    
    Args:
        equipo_id: ID del equipo
    
    Returns:
        Equipo desbloqueado
    
    Raises:
        ValidationError: Si no se puede desbloquear
    """
    try:
        equipo = Equipo.objects.get(pk=equipo_id)
    except Equipo.DoesNotExist:
        raise ValidationError('El equipo no existe')
    
    if equipo.estado != 'MANTENIMIENTO':
        raise ValidationError('El equipo no está en mantenimiento')
    
    # Marcar mantenimientos activos como inactivos
    Mantenimiento.objects.filter(
        equipo=equipo,
        activo=True
    ).update(activo=False, fecha_fin=timezone.now())
    
    # Cambiar estado del equipo
    equipo.estado = 'DISPONIBLE'
    equipo.save()
    
    return equipo


def obtener_equipos_disponibles(laboratorio_id=None):
    """
    Obtener equipos disponibles (no en mantenimiento)
    
    Args:
        laboratorio_id: ID del laboratorio (opcional)
    
    Returns:
        QuerySet de equipos disponibles
    """
    equipos = Equipo.objects.filter(estado='DISPONIBLE')
    if laboratorio_id:
        equipos = equipos.filter(laboratorio_id=laboratorio_id)
    return equipos


def obtener_historial_mantenimientos(equipo_id):
    """
    Obtener historial de mantenimientos de un equipo
    
    Args:
        equipo_id: ID del equipo
    
    Returns:
        QuerySet de mantenimientos ordenados por fecha
    """
    return Mantenimiento.objects.filter(
        equipo_id=equipo_id
    ).order_by('-fecha_inicio')
