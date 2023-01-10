# Generated by Django 4.1.4 on 2023-01-10 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('docker_admin', '0005_balans_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Price',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='count_item',
        ),
        migrations.RemoveField(
            model_name='inventory',
            name='name_item',
        ),
        migrations.AddField(
            model_name='item',
            name='max_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, max_length=5, null=True),
        ),
    ]
