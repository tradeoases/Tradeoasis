# Generated by Django 4.2.4 on 2023-11-30 15:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database_model', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditTrail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='account_type',
            field=models.CharField(choices=[('ADMIN', 'Admin'), ('SUPPORT', 'Support'), ('SUPPLIER', 'Supplier'), ('BUYER', 'Buyer'), ('CUSTOMER', 'Customer')], default='CUSTOMER', max_length=225),
        ),
        migrations.AddField(
            model_name='user',
            name='is_email_activated',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='BusinessProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('business_name', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=255, null=True)),
                ('tin_number', models.CharField(blank=True, max_length=255, null=True)),
                ('vat_number', models.CharField(blank=True, max_length=255, null=True)),
                ('slogan', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('store_url', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('country_code', models.CharField(blank=True, max_length=255, null=True)),
                ('website', models.CharField(blank=True, max_length=255, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
