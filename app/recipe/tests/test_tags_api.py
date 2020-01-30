from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from recipe.serializers import TagSerializer


TAGS_URL = reverse('recipe:tag-list')


class PublicTagsApiTests(TestCase):
    """Testa a API publica de Tags"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Testa a obrigatoriedade da autenticação"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Testa a API privada de Tags"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'fulano@email.com',
            '1234'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Testa se a consulta de tags"""
        Tag.objects.create(user=self.user, name='Almoço')
        Tag.objects.create(user=self.user, name='Jantar')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Testa se a consulta de tags está limitada ao usuário logado"""
        user2 = get_user_model().objects.create_user(
            'fulaninho@email.com',
            '1234'
        )
        Tag.objects.create(user=self.user, name='Almoço')
        Tag.objects.create(user=self.user, name='Jantar')
        other_tag = Tag.objects.create(user=user2, name='Lanche')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertNotIn(other_tag, res.data)

    def test_create_tags_successful(self):
        """Testa a criação das tags"""
        payload = {
            'name': 'Criativas'
        }

        res = self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_create_tags_invalid_payload(self):
        """Testa a criação das tags com payload inválido"""
        payload = {
            'name': ''
        }

        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
