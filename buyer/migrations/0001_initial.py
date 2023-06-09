# Generated by Django 4.2.2 on 2023-06-26 14:38

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth_app', '0001_initial'),
        ('supplier', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WishList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_handled', models.BooleanField(default=False, verbose_name='interest handled')),
                ('viewed_by_supplied', models.BooleanField(default=False, verbose_name='Viewed by supplier')),
                ('created_on', models.DateField(default=django.utils.timezone.now, verbose_name='Created on')),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_app.buyer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.product')),
            ],
        ),
    ]
