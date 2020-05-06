from django.shortcuts import render
from rest_framework import viewsets, status
# Create your views here.
from rest_framework.permissions import AllowAny

from accounts.models import User
from accounts.permissions import IsOwnerOrReadOnly
from accounts.serializers import UserSerializer
from .models import Profile
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'user__username'

    def get_permissions(self):
        """
        Verifica si el usuario es el creador del mismo, de ser
        asi le permite modificarlo
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwnerOrReadOnly]
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]

