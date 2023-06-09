# Generated by Django 4.2.2 on 2023-07-01 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0010_alter_ordershippingdetail_address_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliverycarrier',
            name='tax',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, verbose_name='Tax as a Percentage (00.00)'),
        ),
        migrations.AlterField(
            model_name='deliverycarrier',
            name='tax_ar',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, verbose_name='Tax as a Percentage (00.00)'),
        ),
        migrations.AlterField(
            model_name='deliverycarrier',
            name='tax_de',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, verbose_name='Tax as a Percentage (00.00)'),
        ),
        migrations.AlterField(
            model_name='deliverycarrier',
            name='tax_en',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, verbose_name='Tax as a Percentage (00.00)'),
        ),
        migrations.AlterField(
            model_name='deliverycarrier',
            name='tax_fr',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=3, null=True, verbose_name='Tax as a Percentage (00.00)'),
        ),
        migrations.AlterField(
            model_name='order',
            name='discount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=3, null=True, verbose_name='Discount as a Percentage'),
        ),
        migrations.AlterField(
            model_name='order',
            name='discount_ar',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=3, null=True, verbose_name='Discount as a Percentage'),
        ),
        migrations.AlterField(
            model_name='order',
            name='discount_de',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=3, null=True, verbose_name='Discount as a Percentage'),
        ),
        migrations.AlterField(
            model_name='order',
            name='discount_en',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=3, null=True, verbose_name='Discount as a Percentage'),
        ),
        migrations.AlterField(
            model_name='order',
            name='discount_fr',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=3, null=True, verbose_name='Discount as a Percentage'),
        ),
    ]
