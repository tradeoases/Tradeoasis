# Generated by Django 4.2.2 on 2023-06-26 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_calenderevent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calenderevent',
            name='end',
            field=models.DateField(blank=True, null=True, verbose_name='End Date'),
        ),
    ]
