# Generated by Django 4.1.5 on 2023-01-27 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podres', '0002_service_calendar'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceinstance',
            name='active',
            field=models.BooleanField(default=False),
        ),
    ]
