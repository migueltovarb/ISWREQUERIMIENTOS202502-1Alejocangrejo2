# Arquitectura del Sistema

## Visión General
El sistema sigue una arquitectura monolítica modular basada en **Django**, utilizando **Django REST Framework** para exponer una API que es consumida por el frontend (renderizado por templates de Django con componentes JS interactivos).

## Tecnologías
- **Backend**: Python 3.9+, Django 4.2+
- **API**: Django REST Framework
- **Base de Datos**: SQLite (Desarrollo), PostgreSQL (Producción)
- **Frontend**: HTML5, CSS3 (Custom), JavaScript (Vanilla + FullCalendar.js)
- **Contenedorización**: Docker, Docker Compose

## Estructura de Aplicaciones (Apps)

1.  **core**:
    - Funcionalidades base, mixins, utilidades compartidas.
    - Gestión de modelos base (TimeStampedModel).

2.  **usuarios**:
    - Gestión de autenticación y autorización.
    - Modelo `Usuario` personalizado.
    - Roles y permisos.

3.  **equipos**:
    - Gestión del inventario de laboratorio.
    - Modelos: `Laboratorio`, `Equipo`, `Mantenimiento`.
    - Lógica de bloqueo y disponibilidad.

4.  **reservas**:
    - Núcleo del negocio.
    - Modelo `Reserva`.
    - Lógica de validación de aforo y no-solapamiento.

5.  **calendario**:
    - Vistas y APIs específicas para alimentar el componente FullCalendar.
    - Agregación de datos de disponibilidad.

6.  **notificaciones**:
    - Sistema de mensajería interna y simulación de correos.
    - Modelo `Notificacion`.

7.  **administracion**:
    - Panel de control personalizado para el administrador (Dashboards).

## Diagrama de Componentes (Conceptual)

[Cliente Web] <--> [Nginx/Gunicorn] <--> [Django App]
                                            |
                                            +--> [PostgreSQL]
                                            +--> [Servicio Notificaciones (Simulado)]

## Patrones de Diseño
- **MVC (MVT en Django)**: Separación lógica de Modelos, Vistas y Templates.
- **Repository/Service (Implícito)**: Lógica de negocio compleja encapsulada en métodos de modelos o managers, no en vistas.
- **DTO (Serializers)**: Transformación de datos para la API.
