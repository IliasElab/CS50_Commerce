# Generated by Django 3.2 on 2021-05-17 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0022_alter_bid_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bid',
            options={'ordering': ('value',)},
        ),
    ]
