# Generated by Django 5.1.6 on 2025-03-22 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CoderrBackend_app', '0009_alter_offer_min_delivery_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='min_delivery_time',
            field=models.IntegerField(null=True),
        ),
    ]
