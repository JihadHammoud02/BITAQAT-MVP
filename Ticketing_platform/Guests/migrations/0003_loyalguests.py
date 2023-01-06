# Generated by Django 3.2.16 on 2023-01-05 06:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Guests', '0002_auto_20221226_2213'),
    ]

    operations = [
        migrations.CreateModel(
            name='loyalGuests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventsCount', models.IntegerField(default=0)),
                ('guest', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='guests', to=settings.AUTH_USER_MODEL)),
                ('organizer', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='organizers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
