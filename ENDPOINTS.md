# Endpoints del Sistema

## Autenticación (JWT)
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| POST | `/api/token/` | Obtener par de tokens (access + refresh). |
| POST | `/api/token/refresh/` | Refrescar token de acceso. |

## Usuarios
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| GET | `/api/usuarios/me/` | Obtener perfil del usuario autenticado. |
| PUT | `/api/usuarios/me/` | Actualizar perfil propio. |

## Equipos (Laboratorio)
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| GET | `/api/equipos/` | Listar todos los equipos. Filtros: `estado`, `laboratorio`. |
| GET | `/api/equipos/{id}/` | Detalle de un equipo. |
| POST | `/api/equipos/{id}/mantenimiento/` | **(Admin)** Bloquear equipo por mantenimiento. |
| POST | `/api/equipos/{id}/desbloquear/` | **(Admin)** Desbloquear equipo. |

## Reservas
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| GET | `/api/reservas/` | Listar reservas. Filtros: `fecha_inicio`, `fecha_fin`, `usuario`. |
| POST | `/api/reservas/` | Crear nueva reserva. Requiere: `equipo`, `fecha_inicio`, `fecha_fin`. |
| GET | `/api/reservas/{id}/` | Detalle de reserva. |
| DELETE | `/api/reservas/{id}/` | Cancelar reserva. |

## Calendario (FullCalendar)
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| GET | `/api/calendario/eventos/` | Obtener eventos (reservas + mantenimientos) en formato JSON compatible con FullCalendar. |

## Notificaciones
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| GET | `/api/notificaciones/` | Listar notificaciones del usuario. |
| POST | `/api/notificaciones/{id}/leer/` | Marcar notificación como leída. |

## Administración (Dashboard)
| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| GET | `/api/admin/dashboard/` | Métricas de uso, ocupación actual, etc. |
| PATCH | `/api/admin/config/aforo/` | Modificar aforo máximo del laboratorio. |
