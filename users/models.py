from django.contrib.auth.models import AbstractUser
from django.db import models
from catalog.validators import validate_image_size
from django.core.validators import FileExtensionValidator


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField(upload_to='users/photos', null=True, blank=True, verbose_name='Изображение',
                               validators=[validate_image_size,
                                           FileExtensionValidator(['jpg', 'png'],
                                                                  'Расширение файла « %(extension)s » не допускается. '
                                                                  'Разрешенные расширения: %(allowed_extensions)s .'
                                                                  'Недопустимое расширение!')])
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return self.email
