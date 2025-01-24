from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create a new user'

    def handle(self, *args, **kwargs):
        username = 'david malan'
        password = 'securepassword123'
        email = 'john@example.com'
        first_name = 'david'
        last_name = 'malan'

        if User.objects.filter(username=username).exists():
            self.stdout.write(f"User {username} already exists.")
        else:
            User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name
            )
            self.stdout.write(f"User {username} created successfully.")
