# Generated by Django 3.1.4 on 2020-12-24 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_listing_watchlisted'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='image',
            field=models.ImageField(default='images/no-image.png', upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='desc',
            field=models.TextField(max_length=255),
        ),
    ]
