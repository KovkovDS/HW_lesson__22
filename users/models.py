from django.contrib.auth.models import AbstractUser
from django.db import models
from catalog.validators import validate_image_size
from django.core.validators import FileExtensionValidator
from django_countries.fields import CountryField
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Адрес электронной почты должен быть указан")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, verbose_name='Адрес электронной почты')
    avatar = models.ImageField(upload_to='users/photos', null=True, blank=True, verbose_name='Фото профиля',
                               validators=[validate_image_size,
                                           FileExtensionValidator(['jpg', 'png'],
                                                                  'Расширение файла « %(extension)s » не допускается. '
                                                                  'Разрешенные расширения: %(allowed_extensions)s .'
                                                                  'Недопустимое расширение!')])
    phone_number = models.CharField(max_length=11, blank=True, null=True, verbose_name='Номер телефона')
    country = CountryField(max_length=150, blank=True, blank_label="(Выберите страну)", verbose_name='Страна')
    username = None
    token = models.CharField(max_length=150, blank=True, null=True, verbose_name='Токен для верификации')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
