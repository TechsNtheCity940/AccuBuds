from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    item_type = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    sell_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    terpenes = models.CharField(max_length=255, blank=True, null=True)
    thc_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    received_date = models.DateField(default='2023-09-01')
    item = models.CharField(max_length=255, default='default item')  # New field with default value
    item_description = models.TextField(default='No description available')  # Example from before

    def save(self, *args, **kwargs):
        if not self.sell_price:
            self.sell_price = self.purchase_price * 3
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
