# Generated by Django 4.1.4 on 2022-12-27 13:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('docker_admin', '0002_remove_inventory_item_remove_inventory_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
