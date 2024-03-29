# Generated by Django 4.0 on 2023-07-13 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0013_alter_product_store'),
        ('manager', '0006_alter_notification_category_delete_chatroom'),
    ]

    operations = [
        migrations.AlterField(
            model_name='showroom',
            name='store',
            field=models.ManyToManyField(default=None, related_name='store', to='supplier.Store'),
        ),
    ]
