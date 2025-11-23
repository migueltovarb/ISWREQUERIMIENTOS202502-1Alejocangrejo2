# Flujos del Sistema

## 1. Flujo de Reserva (Estudiante)
1.  **Inicio**: El estudiante accede al sistema y se loguea.
2.  **Visualización**: Accede al módulo "Calendario". El sistema carga las reservas existentes y bloqueos.
3.  **Selección**: El estudiante hace clic en una franja horaria disponible (ej. 10:00 - 12:00).
4.  **Validación Frontend**:
    - ¿La fecha es futura?
    - ¿La duración es válida?
5.  **Solicitud**: Se envía POST a `/api/reservas/`.
6.  **Validación Backend**:
    - ¿El usuario está activo?
    - ¿El equipo existe y está activo?
    - ¿El equipo NO está en mantenimiento en esa fecha?
    - ¿El equipo NO tiene otra reserva en esa franja?
    - ¿El aforo del laboratorio permite más reservas?
7.  **Confirmación**:
    - Si todo es OK: Se crea la reserva. Se envía notificación (simulada). Retorna 201 Created.
    - Si falla: Retorna 400 Bad Request con el motivo.
8.  **Actualización**: El calendario se refresca mostrando la nueva reserva.

## 2. Flujo de Mantenimiento (Administrador)
1.  **Inicio**: Admin accede al panel "Equipos".
2.  **Selección**: Selecciona un equipo y la opción "Bloquear / Mantenimiento".
3.  **Datos**: Ingresa fecha inicio, fecha fin y motivo.
4.  **Procesamiento**:
    - El sistema verifica si existen reservas futuras en ese rango para ese equipo.
    - **Opción A (Estricta)**: Si hay reservas, impide el bloqueo hasta que se cancelen manualmente.
    - **Opción B (Automática)**: El sistema cancela las reservas afectadas y notifica a los estudiantes. (Implementaremos esta).
5.  **Persistencia**: Se crea registro en modelo `Mantenimiento`. El estado del equipo cambia virtualmente a "En Mantenimiento" para esas fechas.
6.  **Feedback**: Se muestra confirmación.

## 3. Flujo de Control de Aforo
1.  **Configuración**: Admin establece `aforo_maximo = 20` en el laboratorio.
2.  **Intento de Reserva**:
    - El sistema cuenta las reservas activas para la franja solicitada.
    - Si `reservas_activas >= aforo_maximo`: Rechaza la solicitud indicando "Aforo Completo".
