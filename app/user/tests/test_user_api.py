from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicUserApiTests(TestCase):
    """Testa a api publica de usuário"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Testa criando um usuário com um payload válido"""
        payload = {
            "email": "fulano@email.com",
            "password": "12345",
            "name": "Fulano da Silva"
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Testa a validação de usuário já cadastrado"""
        payload = {
            "email": "fulano@email.com",
            "password": "12345",
            "name": "Fulano da Silva"
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Testa se a senha tem pelo menos 5 caracteres"""
        payload = {
            "email": "fulano@email.com",
            "password": "1234",
            "name": "Fulano da Silva"
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Testa a geração de token do usuário"""
        payload = {
            "email": "fulano@email.com",
            "password": "1234"
        }
        create_user(**payload)

        res = self.client.post(TOKEN_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_invalid_credentials(self):
        """
            Testa se a geração do token é rejeitada
            quando as credenciais estão inválidas
        """
        create_user(email='fulano@email.com', password='1234')
        payload = {
            "email": "fulano@email.com",
            "password": "12345"
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_no_user(self):
        """
            Testa se a geração do token é rejeitada
            quando o usuário não existe
        """
        payload = {
            "email": "fulano@email.com",
            "password": "12345"
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_missing_field(self):
        """
            Testa se a geração do token é rejeitada
            quando não são passadas as informações
            obrigatórias
        """
        res = self.client.post(TOKEN_URL, {'email': 'fulano@email.com'})

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_retrieve_user_unauthorized(self):
        """Testa se a autenticação é obrigatória para o usuário"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Testes da aplicação que exigem autenticação"""

    def setUp(self):
        self.user = create_user(
            email='fulaninho@email.com',
            password='1234',
            name='Fulaninho da Silva'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Testa se a rota do perfil do usuário"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(
            res.data, {'name': self.user.name, 'email': self.user.email}
        )

    def test_post_profile_not_allowed(self):
        """Testa se a rota do perfil do usuário"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Testa a alteração do perfil do usuário"""
        payload = {
            'name': 'Fulano de Tal',
            'email': 'fulano@email.com'
        }
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertEqual(self.user.name, payload['name'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)
