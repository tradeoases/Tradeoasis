# Generated by Django 4.2.4 on 2023-11-30 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database_model', '0003_audittrail_action_audittrail_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessprofile',
            name='description',
            field=models.TextField(blank=True, max_length=355, null=True),
        ),
    ]
