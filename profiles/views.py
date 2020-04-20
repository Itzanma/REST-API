from django.shortcuts import render
from rest_framework import viewsets, status
# Create your views here.
from accounts.models import User
from accounts.serializers import UserSerializer
from .models import Profile
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

