from django.contrib import admin
from .models import Sale


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'patient', 'user', 'quantity', 'sale_price', 'sale_date', 'terminal_number')
    list_filter = ('sale_date', 'terminal_number')
    readonly_fields = ('sale_date',)
