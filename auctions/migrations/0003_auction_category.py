# Generated by Django 3.2 on 2021-05-09 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auction_bid_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='category',
            field=models.CharField(default=2, max_length=50),
            preserve_default=False,
        ),
    ]
