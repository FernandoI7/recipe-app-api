from django.test import TestCase
from django.contrib.auth import get_user_model


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
