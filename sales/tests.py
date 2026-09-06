"""Smoke tests for the sales app."""
from datetime import date
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase

from inventory.models import Product
from patients.models import Patient
from sales.models import Sale
from users.models import CustomUser


class SaleModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='t', login_pin='1111')
        self.patient = Patient.objects.create(
            patient_name='Test Patient',
            patient_id='P-001',
            prescription_details='pain',
            medical_card_id='MC-001',
            medical_card_expiration=date.today(),
        )
        self.product = Product.objects.create(
            name='Test Bud',
            item_type='flower',
            quantity=10,
            purchase_price=Decimal('20.00'),
        )

    def test_sale_decrements_inventory(self):
        Sale.objects.create(
            product=self.product,
            patient=self.patient,
            user=self.user,
            quantity=3,
            sale_price=Decimal('60.00'),
        )
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 7)

    def test_cannot_sell_more_than_stock(self):
        with self.assertRaises(ValidationError):
            Sale.objects.create(
                product=self.product,
                patient=self.patient,
                user=self.user,
                quantity=999,
                sale_price=Decimal('60.00'),
            )
