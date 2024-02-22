# management/commands/createsuperuserifnotexists.py

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create superuser if not exists'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        username = kwargs.get('username')
        email = kwargs.get('email')
        password = kwargs.get('password')

        if not User.objects.filter(username=username).exists():
            call_command('createsuperuser', username=username, email=email, interactive=False)
            self.stdout.write(self.style.SUCCESS(f'Superuser {username} created'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser {username} already exists'))
