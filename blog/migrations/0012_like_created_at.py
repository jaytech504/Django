# Generated by Django 5.0.4 on 2024-08-14 11:04

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
