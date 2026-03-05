from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Кастомная модель пользователя
    """

    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона', blank=True, null=True)
    telegram_id = models.CharField(max_length=50, verbose_name='ID мессенджера телеграм', blank=True, null=True)
    avatar = models.ImageField(
        upload_to='users/avatars/',
        default='users/avatars/default_ava.png',
        verbose_name='Аватар',
        blank=True,
        null=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.email}'
