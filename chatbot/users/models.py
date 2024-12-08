from django.db import models
import uuid
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    """User için manager sınıfı oluşturuyoruz."""

    def create_user(self, username, email, password=None, **extra_fields):
        """Kullanıcı oluşturmak için."""
        if not email:
            raise ValueError("Email zorunlu bir alandır")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # Şifreleme işlemlerini gerçekleştirmek için
        user.is_active = True  # Aktif yap
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Superuser oluşturmak için."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser "is_staff" alanı True olmalı.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser "is_superuser" alanı True olmalı.')

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Özelleştirilmiş Kullanıcı Modeli"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Admin paneline erişim için
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']  # Burada zorunlu alanlar tanımlanır.

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        """Şifrelemeyi gerçekleştirir."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Şifre doğrulamasını gerçekleştirir."""
        return check_password(raw_password, self.password)
