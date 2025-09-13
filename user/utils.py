import random

from django.conf import settings
from django.core.mail import send_mail


def send_verification_email(email, code):
    send_mail(
        "Email confirmation for theatre app",
        f"Please confirm your email with this code: {code}",
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

def generate_verification_code():
    return random.randint(100000, 999999)
