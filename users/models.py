from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
null_options = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    phone = models.CharField(max_length=35, verbose_name='телефон', **null_options)
    avatar = models.ImageField(upload_to='users/users_avatar', verbose_name='аватар', **null_options)
    token = models.CharField(max_length=100, verbose_name='токен', **null_options)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
