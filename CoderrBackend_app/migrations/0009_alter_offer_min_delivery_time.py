# Generated by Django 5.1.6 on 2025-03-22 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CoderrBackend_app', '0008_alter_offer_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='min_delivery_time',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
