from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import OrderCreateSerializer, OrderSerializer, ProductSerializer


class HealthView(APIView):
    """GET /health - unauthenticated liveness check."""

    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"status": "ok"})


class LoginView(APIView):
    """POST /login - username/password against seeded accounts, returns a token."""

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(
                {"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED
            )
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


class ProductSearchView(generics.ListAPIView):
    """GET /products/search - public, filters by name and/or cooperative."""

    serializer_class = ProductSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Product.objects.all().order_by("id")
        q = self.request.query_params.get("q")
        cooperative = self.request.query_params.get("cooperative")
        if q:
            queryset = queryset.filter(name__icontains=q)
        if cooperative:
            queryset = queryset.filter(cooperative__icontains=cooperative)
        return queryset


class ProductDetailView(generics.RetrieveAPIView):
    """GET /products/<id> - public, 404 when the product does not exist."""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = []
    permission_classes = [AllowAny]


class OrderListCreateView(generics.ListCreateAPIView):
    """GET/POST /orders - authenticated; always scoped to the requesting user."""

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.orders.select_related("product")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return OrderCreateSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(
            {"order_id": serializer.instance.id}, status=status.HTTP_201_CREATED
        )
