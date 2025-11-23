from django.db import models
from core.models import TimeStampedModel

class Laboratorio(TimeStampedModel):
    nombre = models.CharField(max_length=100)
    aforo_maximo = models.PositiveIntegerField(default=20)
    hora_apertura = models.TimeField(default='07:00')
    hora_cierre = models.TimeField(default='22:00')

    def __str__(self):
        return self.nombre

class Equipo(TimeStampedModel):
    ESTADOS = (
        ('DISPONIBLE', 'Disponible'),
        ('MANTENIMIENTO', 'En Mantenimiento'),
        ('FUERA_SERVICIO', 'Fuera de Servicio'),
    )
    codigo = models.CharField(max_length=20, unique=True)
    laboratorio = models.ForeignKey(Laboratorio, on_delete=models.CASCADE, related_name='equipos')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='DISPONIBLE')

    def __str__(self):
        return f"{self.codigo} - {self.get_estado_display()}"

class Mantenimiento(TimeStampedModel):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='mantenimientos')
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    motivo = models.TextField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"Mantenimiento {self.equipo.codigo}"
