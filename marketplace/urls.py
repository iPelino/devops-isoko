from django.urls import path

from . import views

urlpatterns = [
    path("health", views.HealthView.as_view(), name="health"),
    path("login", views.LoginView.as_view(), name="login"),
]
