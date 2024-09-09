from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if User.objects.filter(email='admin@mail.ru').exists():
            pass
        else:
            user = User.objects.create(
                email='admin@mail.ru',
                first_name='Admin',
                last_name='Me',
                is_staff=True,
                is_superuser=True,
            )

            user.set_password('stripedHat80')
            user.save()
