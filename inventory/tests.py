"""Smoke tests for the inventory app."""
from decimal import Decimal

from django.test import TestCase

from inventory.models import Product


class ProductModelTests(TestCase):
    def test_create_product_with_defaults(self):
        p = Product.objects.create(
            name='Test Bud',
            item_type='flower',
            quantity=10,
            purchase_price=Decimal('20.00'),
        )
        self.assertEqual(p.name, 'Test Bud')
        self.assertEqual(p.quantity, 10)
        # 3x markup is a property, not a DB field
        self.assertEqual(p.recommended_sell_price, Decimal('60.00'))

    def test_recommended_sell_price_updates_with_purchase_price(self):
        p = Product.objects.create(
            name='Cheapie',
            item_type='edible',
            quantity=5,
            purchase_price=Decimal('5.00'),
        )
        self.assertEqual(p.recommended_sell_price, Decimal('15.00'))
        p.purchase_price = Decimal('8.00')
        self.assertEqual(p.recommended_sell_price, Decimal('24.00'))
