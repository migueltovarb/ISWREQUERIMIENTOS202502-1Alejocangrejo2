/**
 * Full Calendar Integration
 * Sistema de Gestión de Turnos - Laboratorios
 */

document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');
    if (!calendarEl) return;

    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridWeek',
        locale: 'es',
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        slotMinTime: '07:00:00',
        slotMaxTime: '22:00:00',
        allDaySlot: false,
        selectable: true,
        selectMirror: true,
        editable: false,
        dayMaxEvents: true,

        // Cargar eventos desde la API
        events: function (info, successCallback, failureCallback) {
            fetch('/api/reservas/')
                .then(response => response.json())
                .then(data => {
                    const events = data.map(reserva => ({
                        id: reserva.id,
                        title: `${reserva.equipo_codigo} - ${reserva.usuario_nombre}`,
                        start: reserva.fecha_inicio,
                        end: reserva.fecha_fin,
                        color: getEventColor(reserva.estado),
                        extendedProps: {
                            estado: reserva.estado,
                            equipo_id: reserva.equipo,
                            usuario_id: reserva.usuario
                        }
                    }));
                    successCallback(events);
                })
                .catch(error => {
                    console.error('Error cargando eventos:', error);
                    failureCallback(error);
                });
        },

        // Crear nueva reserva al seleccionar rango
        select: function (info) {
            mostrarModalReserva(info.startStr, info.endStr);
            calendar.unselect();
        },

        // Ver detalles al hacer clic en evento
        eventClick: function (info) {
            mostrarDetallesReserva(info.event);
        },

        // Personalizar contenido del evento
        eventContent: function (arg) {
            return {
                html: `
                    <div class="fc-content">
                        <div class="fc-title">${arg.event.title}</div>
                        <div class="fc-time">${arg.timeText}</div>
                    </div>
                `
            };
        }
    });

    calendar.render();

    // Guardar referencia global al calendario
    window.labCalendar = calendar;
});

/**
 * Obtener color según estado de reserva
 */
function getEventColor(estado) {
    const colors = {
        'ACTIVA': '#059669',      // Verde (success)
        'CANCELADA': '#64748b',   // Gris (neutral)
        'COMPLETADA': '#0284c7'   // Azul (info)
    };
    return colors[estado] || '#3b82f6';
}

/**
 * Mostrar modal para crear nueva reserva
 */
function mostrarModalReserva(fechaInicio, fechaFin) {
    const modal = document.getElementById('modal-reserva');
    if (!modal) return;

    // Setear fechas en el formulario
    document.getElementById('fecha_inicio').value = fechaInicio;
    document.getElementById('fecha_fin').value = fechaFin;

    // Cargar equipos disponibles
    cargarEquiposDisponibles();

    modal.style.display = 'block';
}

/**
 * Cargar equipos disponibles en el select
 */
function cargarEquiposDisponibles() {
    fetch('/api/equipos/disponibles/')
    then(response => response.json())
        .then(equipos => {
            const select = document.getElementById('equipo_id');
            select.innerHTML = '<option value="">Selecciona un equipo</option>';

            equipos.forEach(equipo => {
                const option = document.createElement('option');
                option.value = equipo.id;
                option.textContent = `${equipo.codigo} - ${equipo.laboratorio_name || 'Lab'}`;
                select.appendChild(option);
            });
        })
        .catch(error => console.error('Error cargando equipos:', error));
}

/**
 * Crear reserva (submit del formulario)
 */
async function crearReserva(event) {
    event.preventDefault();

    const formData = {
        equipo: document.getElementById('equipo_id').value,
        fecha_inicio: document.getElementById('fecha_inicio').value,
        fecha_fin: document.getElementById('fecha_fin').value
    };

    try {
        const response = await fetch('/api/reservas/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(formData)
        });

        if (response.ok) {
            mostrarAlerta('Reserva creada exitosamente', 'success');
            cerrarModal('modal-reserva');
            window.labCalendar.refetchEvents(); // Recargar calendario
        } else {
            const error = await response.json();
            mostrarAlerta(error.error || 'Error al crear la reserva', 'danger');
        }
    } catch (error) {
        console.error('Error:', error);
        mostrarAlerta('Error de conexión', 'danger');
    }
}

/**
 * Mostrar detalles de una reserva existente
 */
function mostrarDetallesReserva(event) {
    const detalles = `
        <div class="card">
            <div class="card-header">Detalles de la Reserva</div>
            <p><strong>Equipo:</strong> ${event.title}</p>
            <p><strong>Inicio:</strong> ${formatearFecha(event.start)}</p>
            <p><strong>Fin:</strong> ${formatearFecha(event.end)}</p>
            <p><strong>Estado:</strong> <span class="estado-${event.extendedProps.estado.toLowerCase()}">${event.extendedProps.estado}</span></p>
            ${event.extendedProps.estado === 'ACTIVA' ? '<button class="btn btn-danger btn-sm" onclick="cancelarReserva(' + event.id + ')">Cancelar Reserva</button>' : ''}
        </div>
    `;

    mostrarModal('modal-detalles', detalles);
}

/**
 * Cancelar reserva
 */
async function cancelarReserva(reservaId) {
    if (!confirm('¿Estás seguro de cancelar esta reserva?')) return;

    try {
        const response = await fetch(`/api/reservas/${reservaId}/cancelar/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        if (response.ok) {
            mostrarAlerta('Reserva cancelada', 'success');
            cerrarModal('modal-detalles');
            window.labCalendar.refetchEvents();
        } else {
            mostrarAlerta('Error al cancelar', 'danger');
        }
    } catch (error) {
        console.error('Error:', error);
        mostrarAlerta('Error de conexión', 'danger');
    }
}

/**
 * Utilidades
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function formatearFecha(fecha) {
    return new Date(fecha).toLocaleString('es-ES', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function cerrarModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.style.display = 'none';
}

function mostrarModal(modalId, contenido) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.querySelector('.modal-body').innerHTML = contenido;
        modal.style.display = 'block';
    }
}

function mostrarAlerta(mensaje, tipo = 'info') {
    const alertsContainer = document.getElementById('alerts-container') || document.body;
    const alert = document.createElement('div');
    alert.className = `alert alert-${tipo}`;
    alert.textContent = mensaje;
    alertsContainer.insertBefore(alert, alertsContainer.firstChild);

    setTimeout(() => alert.remove(), 5000);
}
