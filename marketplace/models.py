from django.conf import settings
from django.db import models


class Profile(models.Model):
    """Extends the built-in User with an Isoko-specific role.

    Buyers and cooperative managers share every endpoint in Week 1; only the
    role is modelled now so manager-only endpoints have somewhere to attach
    later.
    """

    class Role(models.TextChoices):
        BUYER = "buyer", "Buyer"
        MANAGER = "manager", "Manager"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="profile",
    )
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.BUYER)

    def __str__(self):
        return f"{self.user.username} ({self.role})"
