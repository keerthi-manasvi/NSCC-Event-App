from django.core.management.base import BaseCommand
from Event.models import Participant
from faker import Faker

class Command(BaseCommand):
    help = "Seed sample participants"

    def handle(self, *args, **options):
        fake = Faker()
        for i in range(10):
            p = Participant.objects.create(name=fake.name(), email=fake.email())
            # generate QR for each
            from Event.views import generate_qr_for_participant
            generate_qr_for_participant(p)
        self.stdout.write(self.style.SUCCESS("Seeded 10 participants"))
