from django.db.models import Count
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from articles.models import Article, Comment
from articles.serializers import ArticleSerializer, CreateArticleSerializer, \
    CommentSerializer, CreateCommentSerializer, ArticleOverviewSerializer
from .permissions import IsOwnerOrReadOnly


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwnerOrReadOnly]

        if self.action in ['list', 'retrieve', 'comments']:
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateCommentSerializer
        return CommentSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    serializer_class = ArticleSerializer
    queryset = Article.objects.annotate(likes_count=Count('likes'))
    lookup_field = 'slug'

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsOwnerOrReadOnly]

        if self.action in ['list', 'retrieve', 'comments']:
            self.permission_classes = [AllowAny]
        return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateArticleSerializer
        return ArticleSerializer

    # Endpoint que retorna los últimos 5 posts
    @action(detail=False, methods=['GET'])
    def latest_posts(self, request):
        articles = Article.published.all().order_by('-created_at')[:5]
        serialized = ArticleOverviewSerializer(articles, many=True)
        if not articles:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                'message': 'No se han publicado árticulos'
            })
        return Response(status=status.HTTP_200_OK, data=serialized.data)

    # Endpoint que regresa los 5 post mas comentados
    @action(detail=False, methods=['GET'])
    def most_comment(self, request):
        articles = Article.published.all().order_by('-comments')[:5]
        serialized = ArticleOverviewSerializer(articles, many=True)
        if not articles:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                'message': 'No se han publicado árticulos'
            })
        return Response(status=status.HTTP_200_OK, data=serialized.data)

    # Endpoint que regresa los 5 post mas votados
    @action(detail=False, methods=['GET'])
    def most_likes(self, request):
        articles = Article.published.all().order_by('-likes')[:5]
        serialized = ArticleOverviewSerializer(articles, many=True)
        if not articles:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                'message': 'No se han publicado árticulos'
            })
        return Response(status=status.HTTP_200_OK, data=serialized.data)
