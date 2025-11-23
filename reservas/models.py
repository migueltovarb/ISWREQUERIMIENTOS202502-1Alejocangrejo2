from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.utils import timezone
from core.models import TimeStampedModel
from equipos.models import Equipo

class Reserva(TimeStampedModel):
    ESTADOS = (
        ('ACTIVA', 'Activa'),
        ('CANCELADA', 'Cancelada'),
        ('COMPLETADA', 'Completada'),
    )
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservas')
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='reservas')
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='ACTIVA')

    class Meta:
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"Reserva {self.usuario} - {self.equipo} ({self.fecha_inicio})"
    
    def clean(self):
        """Validaciones del modelo"""
        super().clean()
        
        # Validar que fecha_fin sea posterior a fecha_inicio
        if self.fecha_fin <= self.fecha_inicio:
            raise ValidationError('La fecha de fin debe ser posterior a la fecha de inicio')
        
        # No permitir reservas en el pasado (solo para nuevas reservas)
        if not self.pk and self.fecha_inicio < timezone.now():
            raise ValidationError('No se pueden crear reservas en el pasado')
        
        # Validar disponibilidad del equipo
        if not self.validar_disponibilidad():
            raise ValidationError('El equipo no está disponible en el horario seleccionado')
        
        # Validar aforo del laboratorio
        if not self.validar_aforo():
            raise ValidationError('El laboratorio ha alcanzado su aforo máximo en este horario')
    
    def validar_disponibilidad(self):
        """
        Verificar que el equipo esté disponible (sin reservas activas en el mismo horario)
        
        Returns:
            bool: True si está disponible, False si hay conflicto
        """
        # Verificar si el equipo está en mantenimiento
        if self.equipo.estado == 'MANTENIMIENTO':
            return False
        
        # Buscar reservas que se solapen en el tiempo
        reservas_solapadas = Reserva.objects.filter(
            equipo=self.equipo,
            estado='ACTIVA'
        ).filter(
            Q(fecha_inicio__lt=self.fecha_fin) & Q(fecha_fin__gt=self.fecha_inicio)
        )
        
        # Excluir la reserva actual si estamos editando
        if self.pk:
            reservas_solapadas = reservas_solapadas.exclude(pk=self.pk)
        
        return not reservas_solapadas.exists()
    
    def validar_aforo(self):
        """
        Verificar que no se exceda el aforo máximo del laboratorio
        
        Returns:
            bool: True si hay espacio, False si se excede el aforo
        """
        laboratorio = self.equipo.laboratorio
        aforo_maximo = laboratorio.aforo_maximo
        
        # Contar reservas activas que se solapen en el tiempo
        reservas_simultaneas = Reserva.objects.filter(
            equipo__laboratorio=laboratorio,
            estado='ACTIVA'
        ).filter(
            Q(fecha_inicio__lt=self.fecha_fin) & Q(fecha_fin__gt=self.fecha_inicio)
        )
        
        # Excluir la reserva actual si estamos editando
        if self.pk:
            reservas_simultaneas = reservas_simultaneas.exclude(pk=self.pk)
        
        count = reservas_simultaneas.count()
        
        return count < aforo_maximo
    
    def cancelar(self):
        """Cancelar la reserva"""
        self.estado = 'CANCELADA'
        self.save()

