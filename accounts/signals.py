from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User


# u1 = User.objects.create_user(username='admin', email='', password='')


@receiver(post_save, sender=User)
def register_new_users(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject='New User',
            from_email=settings.EMAIL_HOST_USER,
            message=f'<h1>New User {instance.username} Welcome!<h1>',
            recipient_list=[instance.email],
            fail_silently=False,
        )

