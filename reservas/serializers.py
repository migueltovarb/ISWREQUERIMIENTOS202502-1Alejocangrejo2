from rest_framework import serializers
from django.utils import timezone
from .models import Reserva
from equipos.models import Equipo

class ReservaSerializer(serializers.ModelSerializer):
    usuario_nombre = serializers.CharField(source='usuario.username', read_only=True)
    equipo_codigo = serializers.CharField(source='equipo.codigo', read_only=True)

    class Meta:
        model = Reserva
        fields = '__all__'
        read_only_fields = ('usuario', 'estado')

    def validate(self, data):
        """
        Validaciones de negocio:
        1. Fecha inicio < Fecha fin
        2. Equipo disponible (no mantenimiento, no reservado)
        3. Aforo del laboratorio (TODO)
        """
        start = data['fecha_inicio']
        end = data['fecha_fin']
        equipo = data['equipo']

        if start >= end:
            raise serializers.ValidationError("La fecha de inicio debe ser anterior a la fecha de fin.")

        if start < timezone.now():
            raise serializers.ValidationError("No se pueden hacer reservas en el pasado.")

        # Validar estado del equipo
        if equipo.estado != 'DISPONIBLE':
            raise serializers.ValidationError(f"El equipo {equipo.codigo} no está disponible.")

        # Validar solapamiento
        solapamientos = Reserva.objects.filter(
            equipo=equipo,
            estado='ACTIVA',
            fecha_inicio__lt=end,
            fecha_fin__gt=start
        )
        if solapamientos.exists():
            raise serializers.ValidationError("El equipo ya está reservado en ese horario.")

        return data
