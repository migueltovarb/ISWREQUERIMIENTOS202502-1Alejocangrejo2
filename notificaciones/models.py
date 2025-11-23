from django.db import models
from django.conf import settings
from core.models import TimeStampedModel

class Notificacion(TimeStampedModel):
    """
    Notificaciones internas del sistema (campana en navbar)
    """
    TIPOS = (
        ('RESERVA_CREADA', 'Reserva Creada'),
        ('RESERVA_CANCELADA', 'Reserva Cancelada'),
        ('EQUIPO_BLOQUEADO', 'Equipo en Mantenimiento'),
        ('EQUIPO_DISPONIBLE', 'Equipo Disponible'),
        ('AFORO_MODIFICADO', 'Aforo Modificado'),
        ('ALERTA_SISTEMA', 'Alerta del Sistema'),
    )
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notificaciones'
    )
    tipo = models.CharField(max_length=30, choices=TIPOS)
    mensaje = models.TextField()
    leida = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.usuario.username}"
    
    def marcar_leida(self):
        """Marcar notificación como leída"""
        self.leida = True
        self.save()


class CorreoSimulado(TimeStampedModel):
    """
    Simulación de correos electrónicos
    No se envían realmente, se guardan en DB para tracking
    """
    ESTADOS = (
        ('PENDIENTE', 'Pendiente'),
        ('ENVIADO', 'Enviado'),
        ('FALLIDO', 'Fallido'),
    )
    
    destinatario = models.EmailField()
    asunto = models.CharField(max_length=200)
    cuerpo = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    intentos = models.PositiveIntegerField(default=0)
    fecha_envio = models.DateTimeField(null=True, blank=True)
    error = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.asunto} - {self.destinatario} ({self.estado})"
    
    def reintentar_envio(self):
        """Simular reintento de envío"""
        from django.utils import timezone
        self.intentos += 1
        self.estado = 'ENVIADO'
        self.fecha_envio = timezone.now()
        self.save()
        return True
