from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin


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
