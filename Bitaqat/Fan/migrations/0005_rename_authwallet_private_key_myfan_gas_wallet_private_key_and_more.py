# Generated by Django 4.1.4 on 2024-01-17 00:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Fan", "0004_feedback_q3_feedback_q4_feedback_q5_feedback_q6"),
    ]

    operations = [
        migrations.RenameField(
            model_name="myfan",
            old_name="AuthWallet_private_key",
            new_name="Gas_Wallet_private_key",
        ),
        migrations.RenameField(
            model_name="myfan",
            old_name="AuthWallet_public_key",
            new_name="Gas_Wallet_public_key",
        ),
        migrations.RenameField(
            model_name="myfan",
            old_name="private_key",
            new_name="NFT_Wallet_private_key",
        ),
        migrations.RenameField(
            model_name="myfan",
            old_name="public_key",
            new_name="NFT_Wallet_public_key",
        ),
        migrations.RemoveField(
            model_name="myfan",
            name="AuthWallet_busy",
        ),
        migrations.RemoveField(
            model_name="myfan",
            name="has_received_matic",
        ),
    ]