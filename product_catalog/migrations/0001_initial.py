# Generated by Django 5.1.1 on 2024-10-26 03:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_dashboard', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car_name', models.CharField(max_length=100)),
                ('brand', models.CharField(max_length=100)),
                ('year', models.PositiveIntegerField()),
                ('mileage', models.PositiveIntegerField()),
                ('location', models.CharField(max_length=100)),
                ('transmission', models.CharField(choices=[('Manual', 'Manual'), ('Automatic', 'Automatic')], max_length=10)),
                ('plate_type', models.CharField(choices=[('Even', 'Even'), ('Odd', 'Odd')], max_length=10)),
                ('rear_camera', models.BooleanField(default=False)),
                ('sun_roof', models.BooleanField(default=False)),
                ('auto_retract_mirror', models.BooleanField(default=False)),
                ('electric_parking_brake', models.BooleanField(default=False)),
                ('map_navigator', models.BooleanField(default=False)),
                ('vehicle_stability_control', models.BooleanField(default=False)),
                ('keyless_push_start', models.BooleanField(default=False)),
                ('sports_mode', models.BooleanField(default=False)),
                ('camera_360_view', models.BooleanField(default=False)),
                ('power_sliding_door', models.BooleanField(default=False)),
                ('auto_cruise_control', models.BooleanField(default=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=15)),
                ('instalment', models.DecimalField(decimal_places=2, max_digits=15)),
                ('image_url', models.URLField(blank=True)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('seller_buat_dashboard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_dashboard.sellerprofile')),
            ],
        ),
    ]
