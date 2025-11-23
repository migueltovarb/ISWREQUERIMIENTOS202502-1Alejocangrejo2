/**
 * Panel de Administración
 * Sistema de�Gestión de Turnos - Laboratorios
 */

// Cargar estadísticas al iniciar
document.addEventListener('DOMContentLoaded', function () {
    cargarEstadisticas();
    cargarLaboratorios();
    cargarEquipos();
    cargarReservasDia();

    // Actualizar cada 30 segundos
    setInterval(cargarEstadisticas, 30000);
});

/**
 * Cargar estadísticas del dashboard
 */
async function cargarEstadisticas() {
    try {
        // Reservas de hoy
        const responseReservas = await fetch('/api/reservas/');
        const reservas = await responseReservas.json();

        const hoy = new Date().toISOString().split('T')[0];
        const reservasHoy = reservas.filter(r => r.fecha_inicio.startsWith(hoy));
        document.getElementById('stat-reservas-hoy').textContent = reservasHoy.length;

        // Equipos
        const responseEquipos = await fetch('/api/equipos/');
        const equipos = await responseEquipos.json();

        const disponibles = equipos.filter(e => e.estado === 'DISPONIBLE');
        const mantenimiento = equipos.filter(e => e.estado === 'MANTENIMIENTO');

        document.getElementById('stat-equipos-disponibles').textContent = disponibles.length;
        document.getElementById('stat-equipos-mantenimiento').textContent = mantenimiento.length;

        // Aforo (del primer laboratorio)
        const responseLabs = await fetch('/api/laboratorios/');
        const labs = await responseLabs.json();
        if (labs.length > 0) {
            document.getElementById('stat-aforo-actual').textContent = labs[0].aforo_maximo;
        }
    } catch (error) {
        console.error('Error cargando estadísticas:', error);
    }
}

/**
 * Cargar laboratorios para el select
 */
async function cargarLaboratorios() {
    try {
        const response = await fetch('/api/laboratorios/');
        const labs = await response.json();

        const select = document.getElementById('laboratorio_id');
        select.innerHTML = '<option value="">Selecciona un laboratorio...</option>';

        labs.forEach(lab => {
            const option = document.createElement('option');
            option.value = lab.id;
            option.textContent = `${lab.nombre} (Aforo: ${lab.aforo_maximo})`;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Error cargando laboratorios:', error);
    }
}

/**
 * Cargar tabla de equipos
 */
async function cargarEquipos() {
    try {
        const response = await fetch('/api/equipos/');
        const equipos = await response.json();

        const tbody = document.querySelector('#tabla-equipos tbody');
        tbody.innerHTML = '';

        equipos.forEach(equipo => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${equipo.codigo}</td>
                <td><span class="equipo-${equipo.estado.toLowerCase()}">${equipo.estado_display || equipo.estado}</span></td>
                <td>Laboratorio</td>
                <td>
                    ${equipo.estado === 'DISPONIBLE' ? `
                        <button class="btn btn-danger btn-sm" onclick="mostrarModalBloquear(${equipo.id}, '${equipo.codigo}')">
                            Bloquear
                        </button>
                    ` : equipo.estado === 'MANTENIMIENTO' ? `
                        <button class="btn btn-success btn-sm" onclick="desbloquearEquipo(${equipo.id})">
                            Desbloquear
                        </button>
                    ` : ''}
                </td>
`;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error cargando equipos:', error);
    }
}

/**
 * Cargar reservas del día
 */
async function cargarReservasDia() {
    try {
        const response = await fetch('/api/reservas/');
        const reservas = await response.json();

        const hoy = new Date().toISOString().split('T')[0];
        const reservasHoy = reservas.filter(r => r.fecha_inicio.startsWith(hoy));

        const tbody = document.querySelector('#tabla-reservas-dia tbody');
        tbody.innerHTML = '';

        reservasHoy.forEach(reserva => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${reserva.usuario_nombre}</td>
                <td>${reserva.equipo_codigo}</td>
                <td>${formatearHora(reserva.fecha_inicio)}</td>
                <td>${formatearHora(reserva.fecha_fin)}</td>
                <td><span class="estado-${reserva.estado.toLowerCase()}">${reserva.estado}</span></td>
                <td>
                    ${reserva.estado === 'ACTIVA' ? `
                        <button class="btn btn-danger btn-sm" onclick="cancelarReservaAdmin(${reserva.id})">
                            Cancelar
                        </button>
                    ` : ''}
                </td>
            `;
            tbody.appendChild(row);
        });

        if (reservasHoy.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center">No hay reservas para hoy</td></tr>';
        }
    } catch (error) {
        console.error('Error cargando reservas:', error);
    }
}

/**
 * Modificar aforo del laboratorio
 */
async function modificarAforo(event) {
    event.preventDefault();

    const labId = document.getElementById('laboratorio_id').value;
    const nuevoAforo = document.getElementById('nuevo_aforo').value;

    if (!labId || !nuevoAforo) {
        alert('Debes seleccionar un laboratorio e ingresar nuevo aforo');
        return;
    }

    try {
        const response = await fetch(`/api/laboratorios/${labId}/modificar_aforo/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ aforo_maximo: nuevoAforo })
        });

        if (response.ok) {
            alert('Aforo actualizado exitosamente');
            cargarEstadisticas();
            cargarLaboratorios();
        } else {
            alert('Error al actualizar aforo');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error de conexión');
    }
}

/**
 * Mostrar modal para bloquear equipo
 */
function mostrarModalBloquear(equipoId, equipoCodigo) {
    document.getElementById('equipo_bloqueo_id').value = equipoId;

    // Setear fecha de inicio a ahora
    const ahora = new Date();
    document.getElementById('bloqueo_inicio').value = ahora.toISOString().slice(0, 16);

    // Setear fecha de fin a 1 día después
    const manana = new Date(ahora.getTime() + 24 * 60 * 60 * 1000);
    document.getElementById('bloqueo_fin').value = manana.toISOString().slice(0, 16);

    document.getElementById('modal-bloquear').style.display = 'block';
}

/**
 * Bloquear equipo
 */
async function bloquearEquipo(event) {
    event.preventDefault();

    const equipoId = document.getElementById('equipo_bloqueo_id').value;
    const fechaInicio = document.getElementById('bloqueo_inicio').value;
    const fechaFin = document.getElementById('bloqueo_fin').value;
    const motivo = document.getElementById('bloqueo_motivo').value;

    try {
        const response = await fetch(`/api/equipos/${equipoId}/bloquear/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                fecha_inicio: fechaInicio,
                fecha_fin: fechaFin,
                motivo: motivo
            })
        });

        if (response.ok) {
            alert('Equipo bloqueado exitosamente');
            cerrarModal('modal-bloquear');
            cargarEquipos();
            cargarEstadisticas();
        } else {
            const error = await response.json();
            alert('Error: ' + (error.error || 'No se pudo bloquear'));
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error de conexión');
    }
}

/**
 * Desbloquear equipo
 */
async function desbloquearEquipo(equipoId) {
    if (!confirm('¿Desbloquear este equipo?')) return;

    try {
        const response = await fetch(`/api/equipos/${equipoId}/desbloquear/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        if (response.ok) {
            alert('Equipo desbloqueado');
            cargarEquipos();
            cargarEstadisticas();
        } else {
            alert('Error al desbloquear');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error de conexión');
    }
}

/**
 * Cancelar reserva como admin
 */
async function cancelarReservaAdmin(reservaId) {
    if (!confirm('¿Cancelar esta reserva?')) return;

    try {
        const response = await fetch(`/api/reservas/${reservaId}/cancelar/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        if (response.ok) {
            alert('Reserva cancelada');
            cargarReservasDia();
            cargarEstadisticas();
        } else {
            alert('Error al cancelar');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error de conexión');
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

function formatearHora(fecha) {
    return new Date(fecha).toLocaleTimeString('es-ES', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

function cerrarModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.style.display = 'none';
}
