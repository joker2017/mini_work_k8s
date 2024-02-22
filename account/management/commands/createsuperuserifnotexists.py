from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates a superuser if not exists'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Superuser username')
        parser.add_argument('email', type=str, help='Superuser email')
        parser.add_argument('password', type=str, help='Superuser password')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']
        if not User.objects.filter(username=username).exists():
            print(f"Creating superuser {username}")
            User.objects.create_superuser(username=username, email=email, password=password)
        else:
            print(f"Superuser {username} already exists.")
