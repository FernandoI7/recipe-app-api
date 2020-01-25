from rest_framework import generics

from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Cria um novo usuário"""
    serializer_class = UserSerializer
