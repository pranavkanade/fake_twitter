from rest_framework import serializers

from core.models import Post
from user.serializers import UserSerializer


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'date_created', 'fake_tweet', 'liked_by', 'disliked_by')
        read_only_fields = ('id', 'liked_by', 'disliked_by', 'author')


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'date_created', 'fake_tweet', 'liked_by', 'disliked_by')
        read_only_fields = ('id', 'author')


class PostDetailSerializer(PostSerializer):
    liked_by = UserSerializer(many=True, read_only=True)
    disliked_by = UserSerializer(many=True, read_only=True)
    author = UserSerializer(many=False, read_only=True)
