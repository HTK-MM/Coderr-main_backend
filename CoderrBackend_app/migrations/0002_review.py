# Generated by Django 5.1.6 on 2025-02-26 10:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CoderrBackend_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('business_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='CoderrBackend_app.userprofile')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CoderrBackend_app.userprofile')),
            ],
        ),
    ]
