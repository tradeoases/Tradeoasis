# Generated by Django 4.0.6 on 2022-07-29 21:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("auth_app", "0004_buyer_support_alter_clientprofile_country_code_and_more"),
        ("buyer", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="wishlist",
            name="user",
        ),
        migrations.AddField(
            model_name="wishlist",
            name="buyer",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="auth_app.buyer",
            ),
            preserve_default=False,
        ),
    ]
