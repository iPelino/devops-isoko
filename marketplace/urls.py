from django.urls import path

from . import views

urlpatterns = [
    path("health", views.HealthView.as_view(), name="health"),
    path("metrics", views.MetricsView.as_view(), name="metrics"),
    path("login", views.LoginView.as_view(), name="login"),
    path("products/search", views.ProductSearchView.as_view(), name="product-search"),
    path("products/<int:pk>", views.ProductDetailView.as_view(), name="product-detail"),
    path("orders", views.OrderListCreateView.as_view(), name="orders"),
]
