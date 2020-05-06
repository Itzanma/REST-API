from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action

from articles.models import Article
from articles.serializers import ArticleSerializer, ArticleOverviewSerializer
from votes.models import Vote
from .permissions import IsOwnerOrReadOnly
from .serializers import UserSerializer, CreateUserSerializer
from .models import User, Follow



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
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    lookup_field = 'username'
    def get_permissions(self):
        """
        Verifica si el usuario es el creador del mismo, de ser
        asi le permite modificarlo, cualquier usuario no registrado
        puede crear uno nuevo.
        :return:
        """
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwnerOrReadOnly]
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        return UserSerializer

    # Endpoint para traer los articulos a los que un usuario ha dado like
    @action(detail=True, methods=['GET'])
    def liked_post(self, request, username=None):
        user = self.get_object()
        articles = Article.objects.filter(likes__user=user.id, likes__value=True)
        serialized = ArticleOverviewSerializer(articles, many=True)
        if not articles:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                                'message': 'Este usuario no tiene articulos favoritos'}
                            )
        return Response(status=status.HTTP_200_OK, data=serialized.data)

    # Endpoint para traer los articulos a los usuarios que sigo
    # limitado a 5 articulos
    @action(detail=True, methods=['GET'])
    def followed_users_posts(self, request, username=None):
        user= self.get_object()
        users_followed = Follow.objects.filter(user_from=user.id)

        # Recibo los ids de los usuarios a los que sigo y los agrego
        # a la lista users
        users = []
        for user in users_followed:
            user_id = user.user_to_id
            users.append(user_id)

        articles = Article.objects.filter(author__id__in=users).order_by('-created_at')[:5]
        serialized =ArticleOverviewSerializer(articles, many=True)
        if not articles:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                                'message': 'Este usuario aun no ha seguido a otro'}
                            )
        return Response(status=status.HTTP_200_OK, data=serialized.data)

    # Endpoint para traer todos los usarios que sigo
    @action(detail=True, methods=['GET'])
    def followed_users(self, request, username=None):
        user=self.get_object()

        # Filtro todos los usuarios que sigo
        users_followed = Follow.objects.filter(user_from=user.id)
        users = []
        for user in users_followed:
            user_id = user.user_to_id
            users.append(user_id)

        # Serializo los usuarios que recibi del filtro

        users_followed = User.objects.filter(id__in=users)
        serialized =UserSerializer(users_followed, many=True)
        if not users_followed:
            return Response(status=status.HTTP_404_NOT_FOUND, data= {
                'message': 'Este usuario no sigue a ningún otro'
            })
        return Response(status=status.HTTP_200_OK, data=serialized.data)

    # Endpoint para traer todos los post que un usuario ha realizado
    @action(detail=True, methods=['GET'])
    def all_posts(self, request, username=None):
        user = self.get_object()
        articles = Article.objects.filter(author=user.id)
        serialized = ArticleOverviewSerializer(articles, many=True)
        if not articles:
            return Response(status=status.HTTP_404_NOT_FOUND, data= {
                'message': 'Este usuario no ha publicado ningun articulo'
            })
        return Response(status=status.HTTP_200_OK, data=serialized.data)