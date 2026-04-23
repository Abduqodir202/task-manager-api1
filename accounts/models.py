from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    POSTER = 'poster'
    MODERATOR = 'moderator'


class User(AbstractUser):
    role = models.CharField(max_length=200, choices=UserRole.choices, default=UserRole.POSTER)
    phone_number = models.CharField(max_length=11, blank=True)
    email = models.EmailField(max_length=200, unique=True)

    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "users"
