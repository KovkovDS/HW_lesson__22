from django.core.management.base import BaseCommand
from django.core.management import call_command
from blog.models import BlogArticle


class Command(BaseCommand):
    help = 'Load test data from fixture'

    def handle(self, *args, **kwargs):
        BlogArticle.objects.all().delete()

        call_command('loaddata', 'blog_fixture.json')
        self.stdout.write(self.style.SUCCESS('Successfully loaded data from fixture'))
