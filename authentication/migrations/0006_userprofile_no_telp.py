# Generated by Django 5.1.2 on 2024-10-24 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_alter_userprofile_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='no_telp',
            field=models.CharField(default='-', max_length=12),
        ),
    ]