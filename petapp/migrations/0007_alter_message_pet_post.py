# Generated by Django 5.1.2 on 2024-11-17 18:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0006_petpost_district_petpost_division'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='pet_post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='petapp.petpost'),
        ),
    ]
