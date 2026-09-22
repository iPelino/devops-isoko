from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
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


class Product(models.Model):
    """A product listed by a cooperative.

    Cooperative is a plain text field, not a foreign key, in Week 1 - see
    the scenario data model.
    """

    name = models.TextField()
    cooperative = models.TextField()
    price_rwf = models.IntegerField(
        validators=[MinValueValidator(0)],
        help_text="Whole Rwandan francs. Isoko does not handle fractional RWF.",
    )

    class Meta:
        db_table = "products"

    def __str__(self):
        return f"{self.name} ({self.cooperative})"


class Order(models.Model):
    """A buyer's order for a quantity of a single product."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="orders"
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(50)],
        help_text="1-50 inclusive, per order.",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "orders"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.pk}: {self.product} x{self.quantity}"
