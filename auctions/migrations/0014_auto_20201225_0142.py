# Generated by Django 3.1.4 on 2020-12-24 18:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_auto_20201225_0106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='auctions.listing'),
        ),
    ]
