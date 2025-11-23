# Historias de Usuario

## Estudiantes

### HU-01: Reservar Equipo
**Como** estudiante, **quiero** reservar un equipo de cómputo por una franja horaria específica, **para** asegurar mi lugar en el laboratorio.
- **Criterios de Aceptación**:
    - Debe validar que el equipo esté disponible.
    - No debe permitir reservas si el aforo está completo.
    - Debe confirmar la reserva inmediatamente.

### HU-02: Ver Disponibilidad
**Como** estudiante, **quiero** ver la disponibilidad de equipos en tiempo real en un calendario, **para** planificar mi visita.
- **Criterios de Aceptación**:
    - El calendario debe mostrar franjas libres y ocupadas.
    - Debe actualizarse al cargar la página.

### HU-03: Cancelar Reserva
**Como** estudiante, **quiero** cancelar una reserva previa, **para** liberar el espacio si no voy a asistir.
- **Criterios de Aceptación**:
    - Solo se pueden cancelar reservas futuras.
    - Debe notificar al sistema de la liberación del cupo.

### HU-04: Historial de Reservas
**Como** estudiante, **quiero** ver mi historial de reservas pasadas y futuras, **para** llevar un control de mi uso del laboratorio.

### HU-05: Recibir Notificaciones
**Como** estudiante, **quiero** recibir notificaciones sobre cambios en mis reservas (ej. cancelación por mantenimiento), **para** estar informado.

---

## Administradores

### HU-06: Bloquear Equipos (Mantenimiento)
**Como** administrador, **quiero** bloquear equipos por mantenimiento, **para** evitar que sean reservados cuando no funcionan.
- **Criterios de Aceptación**:
    - Debe permitir ingresar motivo y fechas.
    - Debe cancelar automáticamente reservas afectadas (o notificar).

### HU-07: Desbloquear Equipos
**Como** administrador, **quiero** desbloquear equipos, **para** ponerlos nuevamente a disposición de los estudiantes.

### HU-08: Modificar Aforo
**Como** administrador, **quiero** cambiar el aforo máximo del laboratorio, **para** ajustarme a normativas o disponibilidad de personal.

### HU-09: Gestión de Reservas
**Como** administrador, **quiero** ver todas las reservas y poder cancelarlas si es necesario, **para** mantener el orden en el laboratorio.

### HU-10: Alertas del Sistema
**Como** administrador, **quiero** recibir alertas sobre sobreaforo o fallas, **para** actuar rápidamente.
