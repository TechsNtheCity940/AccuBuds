"""Seed demo data so the app is usable on first run."""
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction

from inventory.models import Product
from patients.models import Patient
from users.models import CustomUser


PRODUCTS = [
    ('Blue Dream (3.5g)', 'flower', 28, 18.00, 56.00, 'myrcene/pinene', 21.50),
    ('OG Kush (3.5g)', 'flower', 14, 22.00, 65.00, 'limonene/caryophyllene', 24.00),
    ('Sour Diesel (1g)', 'flower', 9, 12.00, 36.00, 'terpinolene', 22.00),
    ('Gummy Bears 100mg', 'edible', 40, 4.50, 15.00, '', 10.00),
    ('Chocolate Bar 200mg', 'edible', 22, 8.00, 25.00, '', 10.00),
    ('Live Resin Cart', 'concentrate', 30, 15.00, 50.00, '', 80.00),
    ('Shatter 1g', 'concentrate', 12, 25.00, 75.00, '', 75.00),
    ('CBD Topical Cream', 'topical', 18, 9.00, 30.00, '', 0.30),
]

PATIENTS = [
    ('Alice Johnson', 'P-1001', 'Chronic pain, anxiety', 'MC-9001'),
    ('Bob Martinez', 'P-1002', 'Insomnia, PTSD', 'MC-9002'),
    ('Carol Davis', 'P-1003', 'Migraines, nausea', 'MC-9003'),
]

USERS = [
    # username, password, PIN
    ('techjuan', 'demo1234', '1234'),
    ('manager', 'demo1234', '9999'),
    ('budtender1', 'demo1234', '0420'),
]


class Command(BaseCommand):
    help = 'Seed demo products, patients, and users with PINs for testing.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing demo data first',
        )

    @transaction.atomic
    def handle(self, *args, **opts):
        if opts['reset']:
            self.stdout.write('Resetting demo data...')
            Product.objects.all().delete()
            Patient.objects.all().delete()
            CustomUser.objects.filter(username__in=[u[0] for u in USERS]).delete()

        for name, item_type, qty, cost, sell, terps, thc in PRODUCTS:
            Product.objects.get_or_create(
                name=name,
                defaults=dict(
                    item_type=item_type,
                    quantity=qty,
                    purchase_price=cost,
                    sell_price=sell,
                    terpenes=terps,
                    thc_percentage=thc,
                    received_date=date.today() - timedelta(days=7),
                    item=name.split(' (')[0],
                    item_description=f'{item_type.title()} — {name}',
                ),
            )

        for patient_name, patient_id, script, mc_id in PATIENTS:
            Patient.objects.get_or_create(
                patient_id=patient_id,
                defaults=dict(
                    patient_name=patient_name,
                    prescription_details=script,
                    medical_card_id=mc_id,
                    medical_card_expiration=date.today() + timedelta(days=365),
                ),
            )

        for username, password, pin in USERS:
            u, created = CustomUser.objects.get_or_create(
                username=username,
                defaults=dict(login_pin=pin, email=f'{username}@accubuds.local'),
            )
            u.set_password(password)
            u.login_pin = pin
            u.is_active = True
            u.save()

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {len(PRODUCTS)} products, {len(PATIENTS)} patients, "
            f"{len(USERS)} users. Try logging in with PIN 1234 (techjuan) or 0420 (budtender1)."
        ))
