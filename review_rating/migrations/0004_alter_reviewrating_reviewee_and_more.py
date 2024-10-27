# Generated by Django 5.1.2 on 2024-10-25 13:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review_rating', '0003_alter_reviewrating_id'),
        ('user_dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviewrating',
            name='reviewee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews_received', to='user_dashboard.sellerprofile'),
        ),
        migrations.AlterField(
            model_name='reviewrating',
            name='reviewer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews_posted', to='user_dashboard.buyerprofile'),
        ),
    ]