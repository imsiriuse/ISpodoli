from django.db import migrations, models


def forwards_func(apps, schema_editor):
    bookingsettings = apps.get_model("booking", "BookingSettings")
    db_alias = schema_editor.connection.alias
    bookingsettings.objects.using(db_alias).create(start_time="09:00", end_time="17:00")


def reverse_func(apps, schema_editor):
    # remove the object we created on forwards_func
    bookingsettings = apps.get_model("booking", "BookingSettings")
    db_alias = schema_editor.connection.alias
    bookingsettings.objects.using(db_alias).filter(start_time="09:00", end_time="17:00").delete()


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookingSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_enable', models.BooleanField(default=True)),
                ('confirmation_required', models.BooleanField(default=True)),
                ('disable_weekend', models.BooleanField(default=True)),
                ('available_booking_months', models.IntegerField(default=1, help_text='if 2, user can only book booking for next two months.')),
                ('max_booking_per_day', models.IntegerField(blank=True, null=True)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('period_of_each_booking', models.CharField(
                    choices=[
                        ('5', '5M'),
                        ('10', '10M'),
                        ('15', '15M'),
                        ('20', '20M'),
                        ('25', '25M'),
                        ('30', '30M'),
                        ('35', '35M'),
                        ('40', '40M'),
                        ('45', '45M'),
                        ('60', '1H'),
                        ('75', '1H 15M'),
                        ('90', '1H 30M'),
                        ('105', '1H 45M'),
                        ('120', '2H'),
                        ('150', '2H 30M'),
                        ('180', '3H')
                    ], default='30', help_text='How long each booking take.', max_length=3)),
                ('max_booking_per_time', models.IntegerField(default=1, help_text='how much booking can be book for each time.')),
            ],
        ),
        # Create base booking_settings for first time
        migrations.RunPython(forwards_func, reverse_func),
    ]
