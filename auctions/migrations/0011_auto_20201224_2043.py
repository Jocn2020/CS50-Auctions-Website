# Generated by Django 3.1.4 on 2020-12-24 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_auto_20201224_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.FileField(default='images/no-image.png', upload_to='images'),
        ),
    ]
