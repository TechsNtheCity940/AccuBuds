# Generated by Django 5.1 on 2024-09-27 01:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='timestamp',
            new_name='sale_date',
        ),
        migrations.RenameField(
            model_name='sale',
            old_name='total_price',
            new_name='sale_price',
        ),
    ]
