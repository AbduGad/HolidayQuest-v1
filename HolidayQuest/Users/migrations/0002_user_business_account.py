# Generated by Django 5.1.4 on 2025-01-07 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='business_account',
            field=models.BooleanField(default=False),
        ),
    ]
