# Generated by Django 4.1.4 on 2023-01-12 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docker_admin', '0007_alter_inventory_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='is_activate',
            field=models.BooleanField(default=True),
        ),
    ]