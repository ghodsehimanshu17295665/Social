# email_utils.py
from django.core.mail import send_mail
from django.conf import settings


def send_simple_email(user):
    subject = 'Welcome to Django Server'
    message = f'Hi {user.username}, thank you for registering on Django Server.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]
    send_mail(subject, message, email_from, recipient_list)
