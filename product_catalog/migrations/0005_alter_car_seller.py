# Generated by Django 5.1.1 on 2024-10-25 10:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_catalog', '0004_merge_0003_alter_car_id_0003_car_image_url'),
        ('user_dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_dashboard.sellerprofile'),
        ),
    ]
