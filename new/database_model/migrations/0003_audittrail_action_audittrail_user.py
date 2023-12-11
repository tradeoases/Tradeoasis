# Generated by Django 4.2.4 on 2023-11-30 15:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database_model', '0002_audittrail_user_account_type_user_is_email_activated_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='audittrail',
            name='action',
            field=models.TextField(blank=True, max_length=355, null=True),
        ),
        migrations.AddField(
            model_name='audittrail',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]