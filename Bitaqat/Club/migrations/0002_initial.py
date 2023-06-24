# Generated by Django 4.1.4 on 2023-06-24 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("Club", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Event",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("datetime", models.DateTimeField()),
                ("place", models.CharField(max_length=500)),
                ("maximum_capacity", models.PositiveIntegerField()),
                ("ticket_price", models.FloatField()),
                ("current_fan_count", models.PositiveIntegerField()),
                ("royalty_rate", models.PositiveIntegerField(default=None)),
                (
                    "banner",
                    models.ImageField(
                        blank=True, default=None, null=True, upload_to=""
                    ),
                ),
                ("team1_name", models.CharField(default=None, max_length=500)),
                ("team2_name", models.CharField(default=None, max_length=500)),
                (
                    "team1_logo",
                    models.ImageField(
                        blank=True, default=None, null=True, upload_to=""
                    ),
                ),
                (
                    "team2_logo",
                    models.ImageField(
                        blank=True, default=None, null=True, upload_to=""
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EventsticketsMinted",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("NFT_owner_address", models.CharField(default=None, max_length=600)),
                ("NFT_token_id", models.CharField(default=None, max_length=600)),
                ("checkIn_Time", models.TimeField(blank=True, null=True)),
            ],
        ),
    ]