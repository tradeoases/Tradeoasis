# Generated by Django 4.0.6 on 2022-08-22 06:04

import auth_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0007_alter_clientprofile_vat_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, default='test/profiledefault.png', null=True, upload_to=auth_app.models.get_file_path, verbose_name='Image'),
        ),
    ]
