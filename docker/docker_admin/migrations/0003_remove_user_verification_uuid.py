# Generated by Django 4.1.4 on 2023-01-26 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docker_admin', '0002_user_is_verified_user_verification_uuid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='verification_uuid',
        ),
    ]
