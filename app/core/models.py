from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        """Cria e salva um novo usuário"""
        if not email:
            raise ValueError("Deve informar um e-mail")
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        """Cria e salva um novo super usuário"""
        if not email:
            raise ValueError("Deve informar um e-mail")
        user = self.model(email=self.normalize_email(email))
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Clase customizada de usuário com e-mail"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=80)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'


class Tag(models.Model):
    """Tag da receita"""
    name = models.CharField(max_length=120)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ingrediente da receita"""
    name = models.CharField(max_length=120)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Model da receita"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING
    )
    title = models.CharField(
        max_length=255
    )
    time_minutes = models.IntegerField()
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )
    link = models.CharField(
        max_length=255,
        blank=True
    )
    ingredients = models.ManyToManyField(
        'Ingredient'
    )
    tags = models.ManyToManyField(
        'Tag'
    )

    def __str__(self):
        return self.title
