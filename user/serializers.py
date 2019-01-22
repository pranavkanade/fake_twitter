from django.contrib.auth import get_user_model
from rest_framework import serializers

from core.models import UserAdvInfo


class UserAdvInfoSerializer(serializers.ModelSerializer):
    """Serialize the adv info model"""

    class Meta:
        model = UserAdvInfo
        fields = ('user_twitter_handle', 'company_name', 'company_location')


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user model"""

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'username', 'password', 'adv_info')
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 4}
        }

    def create(self, validated_data):
        """Create a new user with encrypted password and return the user"""
        return get_user_model().objects.create_user(**validated_data)


class UserDetailSerializer(UserSerializer):
    adv_info = UserAdvInfoSerializer(many=False, read_only=True)
