from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token

from marketplace.models import Product, Profile

SEED_USERS = [
    {"username": "buyer1", "password": "isoko-demo-1", "role": Profile.Role.BUYER},
    {"username": "manager1", "password": "isoko-demo-2", "role": Profile.Role.MANAGER},
]

SEED_PRODUCTS = [
    {
        "name": "Tomatoes",
        "cooperative": "Musanze Growers Cooperative",
        "price_rwf": 500,
    },
    {"name": "Carrots", "cooperative": "Musanze Growers Cooperative", "price_rwf": 400},
    {"name": "Onions", "cooperative": "Nyagatare Farmers Union", "price_rwf": 350},
    {"name": "Potatoes", "cooperative": "Nyagatare Farmers Union", "price_rwf": 300},
    {"name": "Cabbage", "cooperative": "Huye Producers Cooperative", "price_rwf": 250},
    {
        "name": "Green beans",
        "cooperative": "Huye Producers Cooperative",
        "price_rwf": 600,
    },
]


class Command(BaseCommand):
    help = "Seed demo users (with tokens) and products for local development."

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

        for entry in SEED_PRODUCTS:
            product, created = Product.objects.get_or_create(
                name=entry["name"],
                cooperative=entry["cooperative"],
                defaults={"price_rwf": entry["price_rwf"]},
            )
            self.stdout.write(
                f"Seeded product '{product.name}' ({'created' if created else 'exists'})"
            )

        self.stdout.write(self.style.SUCCESS("Seed complete."))
