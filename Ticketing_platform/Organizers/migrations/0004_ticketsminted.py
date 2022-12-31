# Generated by Django 3.2.16 on 2022-12-27 17:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Organizers', '0003_eventscreated'),
    ]

    operations = [
        migrations.CreateModel(
            name='ticketsMinted',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NFT_owner_address', models.CharField(default=None, max_length=600)),
                ('NFT_token_id', models.CharField(default=None, max_length=600)),
                ('NFT_owner_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('event_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Organizers.eventscreated')),
            ],
        ),
    ]