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


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь',
        help_text='Выберите пользователя, который подписывается'
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
        help_text='Выберите автора, на которого подписываются'
    )
    # user = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name='Подписчик'
    # )
    # author = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     related_name='Автор'
    # )
