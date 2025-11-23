from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = (
        ('ESTUDIANTE', 'Estudiante'),
        ('ADMIN', 'Administrador'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='ESTUDIANTE')
    telefono = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"
