# Generated by Django 5.1.4 on 2025-01-07 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_product_category'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='ratings',
            new_name='rating',
        ),
    ]
