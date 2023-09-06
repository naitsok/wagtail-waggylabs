import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Creates superuser within Docker container using environment vars."

    def handle(self, *args, **options):
        User = get_user_model()

        options['username'] = os.environ['DJANGO_SUPERUSER_USERNAME']
        options['email'] = os.environ['DJANGO_SUPERUSER_EMAIL']
        options['password'] = os.environ['DJANGO_SUPERUSER_PASSWORD']

        if not User.objects.filter(username=options['username']).exists():
            User.objects.create_superuser(username=options['username'],
                                          email=options['email'],
                                          password=options['password'])