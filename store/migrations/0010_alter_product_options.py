# Generated by Django 5.1.4 on 2025-01-07 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_product_rating_alter_product_views'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-id'], 'verbose_name_plural': 'Products'},
        ),
    ]