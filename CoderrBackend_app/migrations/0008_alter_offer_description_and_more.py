# Generated by Django 5.1.6 on 2025-03-20 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CoderrBackend_app', '0007_alter_review_reviewer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='offer',
            name='min_delivery_time',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='offer',
            name='min_price',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='location',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='tel',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='working_hours',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
    ]
