# Generated by Django 4.0 on 2023-08-03 23:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_category_tag_ticketstatus_agent_user_rating_article_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='response_time',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
