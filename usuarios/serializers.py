from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'rol', 'telefono')
        read_only_fields = ('id', 'rol') # Rol solo editable por admin
