# Generated by Django 4.1.4 on 2022-12-07 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('docker_admin', '0002_alter_codename_code_alter_codename_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='codename',
            name='owner',
        ),
    ]
