from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientApiTests(TestCase):
    """Testes da API pública de ingredientes"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Testa se o login é obrigatório para acessar o endpoint"""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTests(TestCase):
    """Testes da API privada de ingredientes"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'fulano@email.com',
            '1234'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        """Testa se a consulta de ingredientes"""
        Ingredient.objects.create(user=self.user, name='Arroz')
        Ingredient.objects.create(user=self.user, name='Ovo')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('name')
        serializer = IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_ingredients_limited_to_user(self):
        """
           Testa se a consulta de ingredientes está
           limitada ao usuário logado
        """
        user2 = get_user_model().objects.create_user(
            'fulaninho@email.com',
            '1234'
        )
        Ingredient.objects.create(user=self.user, name='Arroz')
        Ingredient.objects.create(user=self.user, name='Ovo')
        other_ingredient = Ingredient.objects.create(
          user=user2,
          name='Farinha'
        )

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertNotIn(other_ingredient, res.data)

    def test_create_ingredients_successful(self):
        """Testa a criação dos ingredientes"""
        payload = {
            'name': 'Pimenta'
        }

        res = self.client.post(INGREDIENTS_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(exists)

    def test_create_ingredients_invalid_payload(self):
        """Testa a criação dos ingredients com payload inválido"""
        payload = {
            'name': ''
        }

        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
