# Generated by Django 4.1.4 on 2023-06-27 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Club", "0015_alter_mintedtickets_organizer"),
    ]

    operations = [
        migrations.AddField(
            model_name="mintedtickets",
            name="checked",
            field=models.BooleanField(default=False),
        ),
    ]
