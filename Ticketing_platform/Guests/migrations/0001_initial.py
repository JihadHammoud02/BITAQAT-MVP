# Generated by Django 3.2.16 on 2022-12-26 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='myGuests',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_crypto_address', models.CharField(default=None, max_length=600)),
                ('private_crypto_address', models.CharField(default=None, max_length=600)),
            ],
        ),
    ]
