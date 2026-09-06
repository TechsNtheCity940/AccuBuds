from datetime import date
from django.db import models


class Product(models.Model):
    ITEM_TYPES = [
        ('flower', 'Flower'),
        ('edible', 'Edible'),
        ('concentrate', 'Concentrate'),
        ('topical', 'Topical'),
    ]

    name = models.CharField(max_length=255)
    item_type = models.CharField(max_length=50, choices=ITEM_TYPES)
    quantity = models.IntegerField(default=0)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sell_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    terpenes = models.CharField(max_length=255, blank=True, null=True)
    thc_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True
    )
    received_date = models.DateField(default=date.today)
    item = models.CharField(max_length=255, default='default item')
    item_description = models.TextField(default='No description available')

    @property
    def recommended_sell_price(self):
        """3x cost markup — used when no manual sell_price is set."""
        return self.purchase_price * 3

    def __str__(self):
        return self.name
