# Guía de Ejecución del Sistema de Gestión de Turnos

## Requisitos Previos
- Python 3.9+
- Virtualenv (opcional pero recomendado)

## Instalación y Ejecución

1.  **Activar el entorno virtual** (si no está activo):
    ```bash
    # Windows
    .\venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

2.  **Instalar dependencias** (si es necesario):
    ```bash
    pip install -r requirements.txt
    ```

3.  **Ejecutar el servidor**:
    ```bash
    python manage.py runserver
    ```

4.  **Acceder a la aplicación**:
    - Abre tu navegador en `http://127.0.0.1:8000/`

## Credenciales de Acceso

- **Administrador**:
    - Usuario: `admin`
    - Contraseña: `admin123`
    - Dashboard: `http://127.0.0.1:8000/admin-dashboard/` (o vía menú)
    - Admin Django: `http://127.0.0.1:8000/admin/`

## Características Implementadas

- **Gestión de Usuarios**: Estudiantes y Administradores.
- **Gestión de Equipos**: Laboratorios, Equipos, Mantenimiento.
- **Reservas**: Calendario interactivo (FullCalendar), validación de conflictos.
- **Notificaciones**: Sistema básico de notificaciones.
- **API REST**: Endpoints documentados en `ENDPOINTS.md`.
- **Frontend**: Interfaz minimalista con HTML/CSS/JS.

## Estructura del Proyecto

- `config/`: Configuración principal de Django.
- `core/`: Modelos base y vistas generales.
- `usuarios/`: Gestión de usuarios y autenticación.
- `equipos/`: Gestión de laboratorios y equipos.
- `reservas/`: Lógica de reservas.
- `notificaciones/`: Sistema de notificaciones.
- `calendario/`: API para el calendario.
- `administracion/`: Dashboard de administración.
- `templates/`: Plantillas HTML.
- `static/`: Archivos CSS y JS.
