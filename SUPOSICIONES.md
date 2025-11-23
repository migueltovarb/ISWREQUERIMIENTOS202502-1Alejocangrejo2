# Suposiciones del Proyecto

1.  **Un solo Laboratorio**: Para esta versión, se asume que el sistema gestiona un único laboratorio físico, aunque el modelo de datos permitirá escalar a múltiples.
2.  **Horario Fijo**: El laboratorio opera de 07:00 a 22:00. Las reservas fuera de este horario serán rechazadas.
3.  **Autenticación**: Se usarán usuarios locales de Django. No se integrará LDAP real en esta fase.
4.  **Equipos Homogéneos**: Todos los equipos tienen las mismas capacidades (no se distinguirá entre Mac/PC por ahora, salvo por el nombre).
5.  **Duración de Reserva**: Las reservas son por bloques de 1 hora por defecto.

---

# Endpoints de la API (Preliminar)

## Autenticación
- `POST /api/token/`: Obtener JWT.
- `POST /api/token/refresh/`: Refrescar JWT.

## Reservas
- `GET /api/reservas/`: Listar reservas (filtros por fecha, usuario).
- `POST /api/reservas/`: Crear nueva reserva.
- `GET /api/reservas/{id}/`: Detalle.
- `PUT /api/reservas/{id}/`: Modificar.
- `DELETE /api/reservas/{id}/`: Cancelar.

## Equipos
- `GET /api/equipos/`: Listar equipos y su estado.
- `POST /api/equipos/{id}/mantenimiento/`: Bloquear equipo.
- `POST /api/equipos/{id}/desbloquear/`: Desbloquear equipo.

## Laboratorio
- `GET /api/laboratorio/config/`: Ver aforo y horarios.
- `PATCH /api/laboratorio/config/`: Modificar aforo.
