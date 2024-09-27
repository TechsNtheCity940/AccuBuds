from django.db import models
from users.models import CustomUser
from patients.models import Patient
from inventory.models import Product

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.product.quantity -= self.quantity
        self.product.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Sale {self.id} - {self.product.name} to {self.patient.patient_name}'
