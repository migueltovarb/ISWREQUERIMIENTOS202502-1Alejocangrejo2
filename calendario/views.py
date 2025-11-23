from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from reservas.models import Reserva
from equipos.models import Equipo

class CalendarioViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """
        Retorna eventos para FullCalendar.
        """
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        
        reservas = Reserva.objects.filter(estado='ACTIVA')
        if start and end:
            reservas = reservas.filter(fecha_inicio__gte=start, fecha_fin__lte=end)
            
        eventos = []
        for reserva in reservas:
            eventos.append({
                'id': reserva.id,
                'title': f"{reserva.equipo.codigo} - {reserva.usuario.username}",
                'start': reserva.fecha_inicio,
                'end': reserva.fecha_fin,
                'color': '#3788d8', # Azul estándar
            })
            
        # Agregar mantenimientos como eventos rojos
        equipos_mantenimiento = Equipo.objects.filter(estado='MANTENIMIENTO')
        # (Simplificado: en realidad deberíamos consultar el modelo Mantenimiento)
        
        return Response(eventos)
