from django.core.management.base import BaseCommand
from django.core.management import call_command
from users.models import CustomUser


class Command(BaseCommand):
    help = 'Load test data for groups from fixture'

    def handle(self, *args, **kwargs):
        CustomUser.objects.all().delete()

        call_command('loaddata', 'users_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))
