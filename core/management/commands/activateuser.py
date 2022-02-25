from django.core.management import BaseCommand, CommandError
from argparse import ArgumentParser
from core.models import User


class Command(BaseCommand):
    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('username')

    def handle(self, *args, **options):
        try:
            user_obj = User.objects.get(username=options['username'])
            user_obj: User
            user_obj.is_active = True
            user_obj.save()
            print(self.style.SUCCESS("User is active now"))
        except:
            raise CommandError("User name not found")


