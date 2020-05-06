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
        fields = ('id', 'title', 'body', 'author', 'image', 'comments', 'subtitle', 'status')


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.CharField(
        source='author.username',
        read_only=True
    )
    comments = CommentSerializer(read_only=True, many=True)
    likes = serializers.IntegerField(
        source='likes_count',
        read_only=True
    )

    class Meta:
        model = Article
        fields = "__all__"


class ArticleOverviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    print(author)

    class Meta:
        model = Article
        fields = ('id', 'author', 'title', 'slug', 'image')
