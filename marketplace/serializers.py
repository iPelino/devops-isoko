from rest_framework import serializers

from .models import Order, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "cooperative", "price_rwf"]


class OrderSerializer(serializers.ModelSerializer):
    """Read representation for GET /orders - product is the product id."""

    class Meta:
        model = Order
        fields = ["id", "product", "quantity", "created_at"]
        read_only_fields = fields


class OrderCreateSerializer(serializers.ModelSerializer):
    """Write representation for POST /orders.

    Accepts ``product_id`` (matching the OpenAPI contract) and maps it onto
    the model's ``product`` field.
    """

    product_id = serializers.PrimaryKeyRelatedField(
        source="product", queryset=Product.objects.all()
    )

    class Meta:
        model = Order
        fields = ["product_id", "quantity"]

    def validate_quantity(self, value):
        if value < 1 or value > 50:
            raise serializers.ValidationError("Quantity must be between 1 and 50.")
        return value
