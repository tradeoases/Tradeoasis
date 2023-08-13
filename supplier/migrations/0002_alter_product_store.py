# Generated by Django 4.0 on 2023-08-13 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='store',
            field=models.ManyToManyField(blank=True, related_name='store_product', to='supplier.Store'),
        ),
    ]
