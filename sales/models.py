from django.db import models
from django.core.exceptions import ValidationError

from users.models import CustomUser
from patients.models import Patient
from inventory.models import Product


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='sales')
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='sales')
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='sales')
    quantity = models.PositiveIntegerField()
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)
    terminal_number = models.CharField(max_length=20, blank=True, default='')

    def clean(self):
        if self.product_id and self.quantity and self.product.quantity < self.quantity:
            raise ValidationError(
                f'Not enough stock: {self.product.name} has {self.product.quantity}, '
                f'sale wants {self.quantity}'
            )

    def save(self, *args, **kwargs):
        # Validate stock before saving — model-level guard. The atomic
        # select_for_update in the API view is the primary defense; this
        # catches direct ORM / admin saves.
        self.full_clean()
        super().save(*args, **kwargs)
        # Decrement stock after the sale row exists so we never go negative
        # even if super().save() fails midway.
        Product.objects.filter(id=self.product_id).update(
            quantity=models.F('quantity') - self.quantity
        )

    def __str__(self):
        return f'Sale {self.id} - {self.product.name} to {self.patient.patient_name}'
