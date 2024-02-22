from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'site.settings')
django.setup()

class Command(BaseCommand):
    help = 'Создает суперпользователя или обновляет пароль существующего'

    def add_arguments(self, parser):
        parser.add_argument('--username', required=True, help='Имя пользователя')
        parser.add_argument('--email', required=True, help='Email пользователя')
        parser.add_argument('--password', required=True, help='Пароль пользователя')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        try:
            # Попытка найти существующего пользователя
            user = User.objects.get(username=username)

            # Если пользователь найден, обновляем пароль и email
            user.email = email  # Обновляем email, если нужно
            user.set_password(password)  # Обновляем пароль
            user.save()

            self.stdout.write(self.style.SUCCESS(f'Пароль пользователя "{username}" успешно обновлен.'))

        except User.DoesNotExist:
            # Если пользователь не найден, создаем нового суперпользователя
            try:
                User.objects.create_superuser(username=username, email=email, password=password)
                self.stdout.write(self.style.SUCCESS(f'Суперпользователь "{username}" успешно создан.'))
            except ValidationError as e:
                raise CommandError(e)
