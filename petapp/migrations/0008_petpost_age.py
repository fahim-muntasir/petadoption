# Generated by Django 5.1.2 on 2024-12-04 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petapp', '0007_alter_message_pet_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='petpost',
            name='age',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
