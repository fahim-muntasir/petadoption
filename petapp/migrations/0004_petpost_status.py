# Generated by Django 5.1.2 on 2024-11-15 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0003_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='petpost',
            name='status',
            field=models.CharField(choices=[('Active', 'Active'), ('Adopted', 'Adopted')], default='Active', max_length=10),
        ),
    ]
