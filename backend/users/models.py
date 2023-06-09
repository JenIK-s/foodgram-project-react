from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = models.CharField(
        unique=True,
        max_length=150,
        verbose_name='Ваш логин'
    )
    email = models.EmailField(
        unique=True,
        max_length=150,
        verbose_name='Ваш email'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Ваше имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Ваша фамилия'
    )
    is_subcribed = models.BooleanField(
        default=False,
        verbose_name='Подписка на автора'
    )
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
