from django.contrib import admin
from .models import Menu, Booking, Category, Cart, Order, OrderItem

# Register the models to Django admin
admin.site.register(Menu)
admin.site.register(Booking)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
