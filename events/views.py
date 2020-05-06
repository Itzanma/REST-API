from rest_framework import viewsets
from .models import Event, Speaker
from .serializers import EventSerializer, CreateEventSerializer, SpeakerSerializer
from rest_framework.permissions import IsAdminUser

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_serializer_class(self):
        if self.action in ['create','update', 'partial_update']:
            return CreateEventSerializer
        return EventSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return [permission() for permission in self.permission_classes]

class SpeakerViewSet(viewsets.ModelViewSet):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        return [permission() for permission in self.permission_classes]