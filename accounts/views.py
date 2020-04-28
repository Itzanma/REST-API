from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

from articles.models import Article
from articles.serializers import ArticleSerializer
from votes.models import Vote
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

    @action(detail=True, methods=['GET'])
    def liked_post(self, request, pk=None):
        user = self.get_object()
        articles = Article.objects.filter(likes__user=user.id, likes__value=True)
        print(articles)
        serialized = ArticleSerializer(articles, many=True)
        if not articles:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                                'message': 'Este usuario no tiene articulos favoritos'}
                            )
        return Response(status=status.HTTP_200_OK, data=serialized.data)