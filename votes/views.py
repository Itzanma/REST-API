from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from votes.models import Vote
from votes.permissions import IsOwnerOrReadOnly
from votes.serializers import VoteSerializer


class LikesViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwnerOrReadOnly]

        if self.action in ['list', 'retrieve', 'comments']:
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]
