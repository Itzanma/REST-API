from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .permissions import IsOwnerOrReadOnly
from .serializers import UserSerializer, CreateUserSerializer
from .models import User


# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    retrieve:
        Regresa la instancia  de un usuario
    create:
        Crea un nuevo usuario
    list:
        Regresa la lista de Usuario
    update:
        Actualiza un usuario
    partial_update:
        Actualiza un campo en particular de un usuario
    delete:
        Elimina un usuario
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwnerOrReadOnly]
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        return UserSerializer
