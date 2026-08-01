from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from common.service import thread_send_email


# u1 = User.objects.create_user(username='admin', email='', password='')


@receiver(post_save, sender=User)
def register_new_users(sender, instance, created, **kwargs):
    if created:
        thread_send_email(
            to=instance.email,
            subject='Welcome!',
            content='Welcome!',
        )
