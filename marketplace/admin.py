from django.contrib import admin

from .models import Order, Product, Profile

admin.site.register(Profile)
admin.site.register(Product)
admin.site.register(Order)
