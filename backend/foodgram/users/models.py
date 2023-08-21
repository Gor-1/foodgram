from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username",)

    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name="Почта")
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Имя Пользователя")
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Имя")
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Фамилия")

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name="follower",
        verbose_name="Подписчик"
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
        verbose_name="Подписан"
    )

    def __str__(self):
        return f'{self.user.username} - {self.following.username}'

    class Meta:
        verbose_name = 'Подписка на авторов'
        verbose_name_plural = 'Подписки на авторов'
        unique_together = ("user", "following")
