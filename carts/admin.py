from django.contrib import admin

from carts.models import Cart



@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['table', 'product', 'quantity', 'create_timestamp']
