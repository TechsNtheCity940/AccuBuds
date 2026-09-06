from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'item_type', 'quantity', 'purchase_price', 'sell_price', 'thc_percentage')
    list_filter = ('item_type',)
    search_fields = ('name', 'terpenes')
