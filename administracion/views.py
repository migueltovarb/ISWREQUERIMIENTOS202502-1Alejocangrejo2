from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from reservas.models import Reserva
from equipos.models import Equipo, Laboratorio

class DashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_reservas = Reserva.objects.count()
        reservas_activas = Reserva.objects.filter(estado='ACTIVA').count()
        equipos_disponibles = Equipo.objects.filter(estado='DISPONIBLE').count()
        equipos_mantenimiento = Equipo.objects.filter(estado='MANTENIMIENTO').count()
        
        return Response({
            'total_reservas': total_reservas,
            'reservas_activas': reservas_activas,
            'equipos_disponibles': equipos_disponibles,
            'equipos_mantenimiento': equipos_mantenimiento,
        })
