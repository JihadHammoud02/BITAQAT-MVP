# Generated by Django 3.2.16 on 2023-01-06 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Organizers', '0006_alter_eventsticketsminted_checkin_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventsticketsminted',
            name='checkIn_Time',
            field=models.TimeField(auto_now_add=True, null=True),
        ),
    ]
