from django.core.management.base import BaseCommand
from django.utils.timezone import now

class Command(BaseCommand):
    help = 'Показывает текущее время'

    def handle(self, *args, **options):
        current_time = now()
        self.stdout.write(f'Текущее время: {current_time}')
