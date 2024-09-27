from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_type', 'quantity', 'purchase_price', 'recommended_sell_price', 'received_date')
    search_fields = ('name', 'item_type')

admin.site.register(Product, ProductAdmin)
