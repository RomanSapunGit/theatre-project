from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = "Create default superuser"

    def handle(self, *args, **kwargs):
        user = get_user_model()
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "supersecret")
        if not user.objects.filter(email=email).exists():
            user.objects.create_superuser(email=email, password=password)
            self.stdout.write(self.style.SUCCESS("Superuser created"))
        else:
            self.stdout.write("Superuser already exists")