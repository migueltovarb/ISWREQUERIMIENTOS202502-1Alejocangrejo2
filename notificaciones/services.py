from django.utils import timezone
from django.db.models import Q
from .models import Notificacion, CorreoSimulado
from usuarios.models import Usuario

def notificar_usuario(usuario, tipo, mensaje):
    """
    Función de ejemplo: Crear notificación interna para un usuario
    
    Args:
        usuario: Instancia de Usuario
        tipo: Tipo de notificación (RESERVA_CREADA, EQUIPO_BLOQUEADO, etc.)
        mensaje: Texto del mensaje
    
    Returns:
        Notificacion creada
    """
    notificacion = Notificacion.objects.create(
        usuario=usuario,
        tipo=tipo,
        mensaje=mensaje
    )
    return notificacion


def enviar_correo_simulado(destinatario, asunto, cuerpo):
    """
    Función de ejemplo: Simular envío de correo electrónico
    No se envía realmente, solo se guarda en la base de datos
    
    Args:
        destinatario: Email del destinatario
        asunto: Asunto del correo
        cuerpo: Cuerpo del mensaje
    
    Returns:
        CorreoSimulado creado
    """
    correo = CorreoSimulado.objects.create(
        destinatario=destinatario,
        asunto=asunto,
        cuerpo=cuerpo,
        estado='ENVIADO',  # Simular que se envió inmediatamente
        fecha_envio=timezone.now(),
        intentos=1
    )
    return correo


def notificar_reserva_creada(reserva):
    """
    Notificar al usuario cuando se crea una reserva
    
    Args:
        reserva: Instancia de Reserva
    """
    mensaje = f"Tu reserva del equipo {reserva.equipo.codigo} para el {reserva.fecha_inicio.strftime('%d/%m/%Y %H:%M')} ha sido confirmada."
    
    # Notificación interna
    notificar_usuario(
        usuario=reserva.usuario,
        tipo='RESERVA_CREADA',
        mensaje=mensaje
    )
    
    # Correo simulado
    if reserva.usuario.email:
        enviar_correo_simulado(
            destinatario=reserva.usuario.email,
            asunto='Reserva Confirmada',
            cuerpo=f"""
            Hola {reserva.usuario.get_full_name() or reserva.usuario.username},
            
            {mensaje}
            
            Detalles:
            - Equipo: {reserva.equipo.codigo}
            - Laboratorio: {reserva.equipo.laboratorio.nombre}
            - Inicio: {reserva.fecha_inicio.strftime('%d/%m/%Y %H:%M')}
            - Fin: {reserva.fecha_fin.strftime('%d/%m/%Y %H:%M')}
            
            Gracias por usar nuestro sistema.
            """
        )


def notificar_reserva_cancelada(reserva):
    """
    Notificar al usuario cuando se cancela una reserva
    
    Args:
        reserva: Instancia de Reserva
    """
    mensaje = f"Tu reserva del equipo {reserva.equipo.codigo} para el {reserva.fecha_inicio.strftime('%d/%m/%Y %H:%M')} ha sido cancelada."
    
    # Notificación interna
    notificar_usuario(
        usuario=reserva.usuario,
        tipo='RESERVA_CANCELADA',
        mensaje=mensaje
    )
    
    # Correo simulado
    if reserva.usuario.email:
        enviar_correo_simulado(
            destinatario=reserva.usuario.email,
            asunto='Reserva Cancelada',
            cuerpo=f"""
            Hola {reserva.usuario.get_full_name() or reserva.usuario.username},
            
            {mensaje}
            
            Puedes hacer una nueva reserva cuando lo necesites.
            """
        )


def notificar_equipo_bloqueado(equipo, mantenimiento):
    """
    Notificar a estudiantes con reservas afectadas cuando un equipo se bloquea
    
    Args:
        equipo: Instancia de Equipo bloqueado
        mantenimiento: Instancia de Mantenimiento
    """
    from reservas.models import Reserva
    
    # Obtener reservas afectadas (activas en el rango de mantenimiento)
    reservas_afectadas = Reserva.objects.filter(
        equipo=equipo,
        estado='ACTIVA',
        fecha_inicio__lt=mantenimiento.fecha_fin,
        fecha_fin__gt=mantenimiento.fecha_inicio
    )
    
    for reserva in reservas_afectadas:
        mensaje = f"El equipo {equipo.codigo} ha entrado en mantenimiento. Tu reserva del {reserva.fecha_inicio.strftime('%d/%m/%Y %H:%M')} ha sido cancelada. Motivo: {mantenimiento.motivo}"
        
        # Notificación interna
        notificar_usuario(
            usuario=reserva.usuario,
            tipo='EQUIPO_BLOQUEADO',
            mensaje=mensaje
        )
        
        # Correo simulado
        if reserva.usuario.email:
            enviar_correo_simulado(
                destinatario=reserva.usuario.email,
                asunto='Reserva Cancelada - Equipo en Mantenimiento',
                cuerpo=f"""
                Hola {reserva.usuario.get_full_name() or reserva.usuario.username},
                
                Lamentamos informarte que {mensaje}
                
                Período de mantenimiento:
                - Inicio: {mantenimiento.fecha_inicio.strftime('%d/%m/%Y %H:%M')}
                - Fin estimado: {mantenimiento.fecha_fin.strftime('%d/%m/%Y %H:%M')}
                
                Por favor, selecciona otro equipo para tu reserva.
                """
            )


def notificar_aforo_modificado(laboratorio, nuevo_aforo, administrador):
    """
    Notificar a administradores cuando se modifica el aforo
    
    Args:
        laboratorio: Instancia de Laboratorio
        nuevo_aforo: Nuevo valor de aforo
        administrador: Usuario que hizo el cambio
    """
    # Notificar a todos los administradores
    admins = Usuario.objects.filter(rol='ADMIN')
    
    mensaje = f"El aforo del laboratorio {laboratorio.nombre} ha sido modificado a {nuevo_aforo} por {administrador.username}."
    
    for admin in admins:
        if admin != administrador:  # No notificar al que hizo el cambio
            notificar_usuario(
                usuario=admin,
                tipo='AFORO_MODIFICADO',
                mensaje=mensaje
            )


def obtener_notificaciones_no_leidas(usuario):
    """
    Obtener cantidad de notificaciones no leídas de un usuario
    
    Args:
        usuario: Instancia de Usuario
    
    Returns:
        int: Cantidad de notificaciones no leídas
    """
    return usuario.notificaciones.filter(leida=False).count()
