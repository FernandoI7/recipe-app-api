from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer dos objetos de Usuário"""

    def create(self, validated_data):
        """Cria e retorna um novo usuário"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Altera um usuário"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user

    class Meta:
        model = get_user_model()
        fields = ("email", "password", "name")
        extra_kwargs = {
            "password": {
                "write_only": True,
                "min_length": 5
            }
        }


class AuthTokenSerializer(serializers.Serializer):
    """Serializer do objeto de autenticação do usuário"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Valida e autentica o usuário"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg = _("Usuário ou senha inválidos")
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs
