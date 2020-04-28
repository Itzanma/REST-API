from rest_framework import serializers

from articles.models import Article, Comment
from accounts.models import User
from votes.models import Vote
from votes.serializers import VoteSerializer


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'author', 'body', 'parent_comment', 'created_at')


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('author', 'body', 'parent_comment', 'article')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class CreateArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('id', 'title', 'body', 'author', 'image', 'comments', 'subtitle')


class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Article
        fields = "__all__"

    def get_likes(self, obj):
        return obj.likes.filter(value=True).count()