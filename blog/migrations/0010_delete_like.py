# Generated by Django 5.0.4 on 2024-08-11 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_post_likes'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Like',
        ),
    ]