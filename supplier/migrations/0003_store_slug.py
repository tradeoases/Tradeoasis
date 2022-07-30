# Generated by Django 4.0.6 on 2022-07-30 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0002_alter_service_supplier_alter_store_supplier'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True, verbose_name='Safe Url'),
        ),
    ]
