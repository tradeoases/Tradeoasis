# Generated by Django 4.2.2 on 2023-06-27 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0006_alter_orderproductvariation_cart_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='currency',
            field=models.CharField(blank=True, max_length=6, null=True, verbose_name='Currency'),
        ),
    ]
