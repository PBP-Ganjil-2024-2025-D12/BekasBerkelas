# Generated by Django 5.1.2 on 2024-10-24 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_question_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.CharField(choices=[('UM', 'Umum'), ('JB', 'Jual Beli'), ('TT', 'Tips & Trik'), ('SA', 'Santai')], default='UM', max_length=2),
        ),
    ]
