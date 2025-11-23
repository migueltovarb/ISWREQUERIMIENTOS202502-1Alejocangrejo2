from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import UsuarioSerializer

User = get_user_model()

class UsuarioViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint para ver usuarios.
    """
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.rol == 'ADMIN':
            return User.objects.all()
        return User.objects.filter(id=user.id)
