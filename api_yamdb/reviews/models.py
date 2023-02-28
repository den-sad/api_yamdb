from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    ROLES_CHOISES = [
        ("user", "user"),
        ("moderator", "moderator"),
        ("admin", "admin"),
    ]
    username = models.CharField(max_length=150, unique=True,
                                validators=[
                                    RegexValidator(
                                        regex='^[\\w.@+-]+\\Z',
                                        message='Набор символов неверный',
                                    ),
                                ])
    email = models.EmailField('email address', blank=False, unique=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        max_length=10,
        choices=ROLES_CHOISES,
        default="user",
    )

    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ['pk']

    def __str__(self):
        return self.username
