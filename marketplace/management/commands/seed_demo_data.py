from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token

from marketplace.models import Profile

SEED_USERS = [
    {"username": "buyer1", "password": "isoko-demo-1", "role": Profile.Role.BUYER},
    {"username": "manager1", "password": "isoko-demo-2", "role": Profile.Role.MANAGER},
]


class Command(BaseCommand):
    help = "Seed demo users (with tokens) for local development."

    def handle(self, *args, **options):
        for entry in SEED_USERS:
            user, created = User.objects.get_or_create(username=entry["username"])
            if created:
                user.set_password(entry["password"])
                user.save()
            Profile.objects.update_or_create(
                user=user, defaults={"role": entry["role"]}
            )
            token, _ = Token.objects.get_or_create(user=user)
            self.stdout.write(
                f"Seeded user '{user.username}' (role={entry['role']}), token={token.key}"
            )

        self.stdout.write(self.style.SUCCESS("Seed complete."))
