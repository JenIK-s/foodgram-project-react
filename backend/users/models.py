from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    username = models.CharField(
        unique=True,
        max_length=settings.MAX_LENGTH,
        min_length=5,
        verbose_name='Ваш логин'
    )
    email = models.EmailField(
        unique=True,
        max_length=settings.MAX_LENGTH,
        verbose_name='Ваш email'
    )
    first_name = models.CharField(
        max_length=settings.MAX_LENGTH,
        verbose_name='Ваше имя'
    )
    last_name = models.CharField(
        max_length=settings.MAX_LENGTH,
        verbose_name='Ваша фамилия'
    )
    is_subcribed = models.BooleanField(
        default=False,
        verbose_name='Подписка на автора'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Subscription(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Избранный автор',
    )

    class Meta:
        verbose_name = 'Избранный автор'
        verbose_name_plural = 'Избранные авторы'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'], name='unique_relationships'
            ),
            models.CheckConstraint(
                name='prevent_self_follow',
                check=~models.Q(user=models.F('author')),
            ),
        ]

    def __str__(self):
        return f'{self.user} {self.author}'
