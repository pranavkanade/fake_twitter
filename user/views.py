from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from user.serializers import UserSerializer


class HelloViewAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class CreateUserViewAPI(generics.CreateAPIView):
    """Create new user using api"""
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
