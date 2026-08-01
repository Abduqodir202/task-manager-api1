import pyotp
from django.contrib.auth.models import AbstractUser
import random
from django.db import models
from django.utils import timezone
from datetime import timedelta


class UserRole(models.TextChoices):
    POSTER = 'poster'
    MODERATOR = 'moderator'


class User(AbstractUser):
    role = models.CharField(max_length=200, choices=UserRole.choices, default=UserRole.POSTER)
    phone_number = models.CharField(max_length=11, blank=True)
    email = models.EmailField(max_length=200, unique=True)
    amount = models.PositiveIntegerField(default=0)
    is_2fa_enabled = models.BooleanField(default=False)  # 2FA yoqilganmi?
    totp_secret = models.CharField(max_length=32, blank=True, null=True)  # Google Authenticator kaliti

    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = ["username"]

    def generate_totp_secret(self):
        """Foydalanuvchi uchun yangi 2FA kalit generatsiya qilish."""
        self.totp_secret = pyotp.random_base32()
        self.save()

    def verify_otp(self, otp_code):
        """Foydalanuvchining kiritgan kodini tekshirish."""
        if not self.totp_secret:
            return False
        totp = pyotp.TOTP(self.totp_secret)
        return totp.verify(otp_code, valid_window=3)

    class Meta:
        db_table = "users"


def generate_code():
    # 100000 dan 999999 gacha random son
    return random.randint(100000, 999999)


def exp_time_now():
    # Hozirdan 2 daqiqa keyin muddati tugaydi
    return timezone.now() + timedelta(minutes=2)


class VerificationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='verification_codes')
    code = models.PositiveIntegerField(default=generate_code)
    expired_date = models.DateTimeField(default=exp_time_now)

    def is_valid(self):
        """Kodning muddati o'tmagan bo'lsa True qaytaradi."""
        return timezone.now() <= self.expired_date

    def __str__(self):
        return f"{self.user.username} — Kod: {self.code}"
