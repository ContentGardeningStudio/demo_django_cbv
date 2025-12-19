from django.core.management.base import BaseCommand
from orders.models import Order
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Create sample orders for testing'

    def handle(self, *args, **kwargs):
        for _ in range(50):
            Order.objects.create(
                name=fake.company(),
                total=fake.random_number(digits=3)
            )

        self.stdout.write(self.style.SUCCESS('Successfully created sample orders'))