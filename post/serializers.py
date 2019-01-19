from rest_framework import serializers
from core.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'date_time', 'tweet')
        read_only_fields = ('id',)

