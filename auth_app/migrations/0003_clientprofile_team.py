# Generated by Django 4.2.2 on 2023-07-05 13:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0002_clientprofile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientprofile',
            name='team',
            field=models.ManyToManyField(blank=True, related_name='team_members', to=settings.AUTH_USER_MODEL),
        ),
    ]