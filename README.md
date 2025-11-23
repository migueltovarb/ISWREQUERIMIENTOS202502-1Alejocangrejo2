# Sistema de Gestión de Turnos en Laboratorios

Sistema web para la administración eficiente de reservas de equipos de cómputo en laboratorios universitarios.

## Características
- **Gestión de Reservas**: Calendario interactivo para reservar por franjas horarias.
- **Control de Aforo**: Validación automática de capacidad del laboratorio.
- **Mantenimiento**: Bloqueo de equipos por administradores.
- **Notificaciones**: Sistema simulado de alertas y correos.
- **API REST**: Backend robusto con Django REST Framework.

## Tecnologías
- Django 4.2
- Django REST Framework
- FullCalendar.js
- Docker & PostgreSQL

## Instalación y Ejecución

### Requisitos
- Docker y Docker Compose
- O Python 3.9+ y SQLite

### Ejecución con Docker (Recomendado)
1. Clonar el repositorio.
2. Ejecutar:
   ```bash
   docker-compose up --build
   ```
3. Acceder a `http://localhost:8000`.

### Ejecución Manual
1. Crear entorno virtual: `python -m venv venv`
2. Activar entorno: `source venv/bin/activate` (Linux/Mac) o `venv\Scripts\activate` (Windows)
3. Instalar dependencias: `pip install -r requirements.txt`
4. Migrar base de datos: `python manage.py migrate`
5. Crear superusuario: `python manage.py createsuperuser`
6. Correr servidor: `python manage.py runserver`

## Documentación
La documentación detallada se encuentra en la carpeta `DOCUMENTACION/`:
- [Historias de Usuario](DOCUMENTACION/HistoriasDeUsuario.md)
- [Arquitectura](DOCUMENTACION/Arquitectura.md)
- [Flujos del Sistema](DOCUMENTACION/FlujosDelSistema.md)
