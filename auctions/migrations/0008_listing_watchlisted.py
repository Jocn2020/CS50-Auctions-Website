# Generated by Django 3.1.4 on 2020-12-24 01:13

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_listing_current_holder'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watchlisted',
            field=models.ManyToManyField(blank=True, default=None, related_name='watchlisted', to=settings.AUTH_USER_MODEL),
        ),
    ]
