# Generated by Django 2.2.14 on 2020-07-17 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_remove_auctionimage_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionimage',
            name='image',
            field=models.ImageField(upload_to='media/%Y/%m/%d/'),
        ),
    ]