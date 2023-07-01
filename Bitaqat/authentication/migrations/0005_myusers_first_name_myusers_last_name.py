# Generated by Django 4.1.4 on 2023-06-24 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0004_remove_myusers_first_name_remove_myusers_last_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="myusers",
            name="first_name",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="first name"
            ),
        ),
        migrations.AddField(
            model_name="myusers",
            name="last_name",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="last name"
            ),
        ),
    ]
