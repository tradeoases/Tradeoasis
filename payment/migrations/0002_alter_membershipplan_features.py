# Generated by Django 4.0 on 2023-07-13 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membershipplan',
            name='features',
            field=models.ManyToManyField(related_name='features_list', to='payment.Feature'),
        ),
    ]
