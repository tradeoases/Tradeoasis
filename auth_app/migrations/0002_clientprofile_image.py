# Generated by Django 4.2.2 on 2023-07-05 08:20

import auth_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientprofile',
            name='image',
            field=models.FileField(default='test/django.png', upload_to=auth_app.models.get_file_path, verbose_name='Business Image'),
        ),
    ]