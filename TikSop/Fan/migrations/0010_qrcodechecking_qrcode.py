# Generated by Django 4.1.4 on 2023-06-18 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Fan", "0009_qrcodechecking"),
    ]

    operations = [
        migrations.AddField(
            model_name="qrcodechecking",
            name="Qrcode",
            field=models.ImageField(blank=True, default=None, null=True, upload_to=""),
        ),
    ]
