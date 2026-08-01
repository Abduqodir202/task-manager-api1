from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
import os
from django.conf import settings
import threading


# 1- oddiy send_mail
def send_email(to, subject, content):
    send_mail(
        subject,
        message=content,
        from_email='giyosoripov4@gmail.com',
        recipient_list=[to]
    )


# 2- usul
def send_email_with_class():
    file_path = os.path.join(settings.BASE_DIR, "common/file.pdf")

    email = EmailMessage(
        subject="Fayl bilan email",
        body="Mana biriktirilgan fayl.",
        from_email="giyosoripov4@gmail.com",
        to=["giyosoripov4@gmail.com"],
    )
    with open(file_path, "rb") as f:
        email.attach("file.pdf", f.read(), "application/pdf")
    email.send()


# 3-usul

def send_email_multi_alternatives():
    file_path = os.path.join(settings.BASE_DIR, "common/file.pdf")

    subject = "Fayl bilan email"
    text_content = "Mana biriktirilgan fayl."
    from_email = settings.EMAIL_HOST_USER
    to = ["giyosoripov4@gmail.com"]

    html_content = """
        <h1 style="color:#3b82f6">Salom!</h1>
        <p>Bu <strong>HTML</strong> email.</p>
        <a href="https://example.com">Saytga o'tish</a>
        """

    email = EmailMultiAlternatives(
        subject, text_content, from_email, to
    )

    email.attach_alternative(html_content, "text/html")

    with open(file_path, "rb") as f:
        email.attach("file.pdf", f.read(), "application/pdf")

    email.send()


def thread_send_email(to, subject, content):
    thread = threading.Thread(target=send_email, args=(to, subject, content))
    thread.start()


def thread_send_email_multi_alternatives():
    thread = threading.Thread(target=send_email_multi_alternatives)
    thread.start()
