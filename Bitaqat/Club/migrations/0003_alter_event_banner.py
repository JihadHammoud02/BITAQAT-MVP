# Generated by Django 5.0.2 on 2024-02-17 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Club", "0002_myclub_royaltyreceiver_private_key"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="banner",
            field=models.ImageField(
                blank=True, default="None", null=True, upload_to="EventsBanner"
            ),
        ),
    ]