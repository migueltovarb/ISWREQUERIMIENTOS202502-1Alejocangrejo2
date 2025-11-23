from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Reserva
from .serializers import ReservaSerializer

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'ADMIN':
            return Reserva.objects.all()
        return Reserva.objects.filter(usuario=user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        reserva = self.get_object()
        if reserva.estado == 'CANCELADA':
            return Response({'error': 'La reserva ya está cancelada'}, status=status.HTTP_400_BAD_REQUEST)
        
        reserva.estado = 'CANCELADA'
        reserva.save()
        return Response({'status': 'Reserva cancelada'}, status=status.HTTP_200_OK)
