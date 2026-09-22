from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import ProductSerializer


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
