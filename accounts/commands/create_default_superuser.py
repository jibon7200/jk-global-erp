from django.core.management.base import BaseCommand
from django.conf import settings
from accounts.models import User


class Command(BaseCommand):
    help = 'Creates the initial Admin superuser from environment variables, if one does not already exist. Safe to run on every deploy.'

    def handle(self, *args, **options):
        username = settings.DEFAULT_SUPERUSER_USERNAME
        password = settings.DEFAULT_SUPERUSER_PASSWORD
        email = settings.DEFAULT_SUPERUSER_EMAIL

        if not username or not password:
            self.stdout.write(self.style.WARNING(
                'DEFAULT_SUPERUSER_USERNAME / DEFAULT_SUPERUSER_PASSWORD not set — skipping.'
            ))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(f'Superuser "{username}" already exists — skipping.')
            return

        user = User.objects.create_superuser(username=username, email=email, password=password)
        user.role = User.Role.ADMIN
        user.save()
        self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully.'))