# Generated by Django 4.1.4 on 2023-06-16 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Club", "0012_myclub_royaltyreceiveraddresse"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="myclub",
            name="RoyaltyReceiverAddresse",
        ),
    ]
