from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='fulano@email.com', password='1234'):
    """Cria um usuário de exemplo"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email(self):
        """Testa se a criação de usuário com email está funcionando"""
        email = "fulano@email.com"
        password = "senha1234"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Testa se o email está normalizado"""
        email = "fulano@EMAIL.COM"
        user = get_user_model().objects.create_user(email, "1234")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Testa se criar um usuário sem e-mail lança um erro"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "1234")

    def test_create_new_superuser(self):
        """Teste a criação de um superusuario"""
        user = get_user_model().objects.create_superuser(
            "fulano@email.com",
            "1234"
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Testa a string da tag"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Almoço'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Testa a string do ingrediente"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Arroz'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Testa a respresentação em string da receita"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Bauru',
            time_minutes=5,
            price=20.0
        )

        self.assertEqual(str(recipe), recipe.title)
