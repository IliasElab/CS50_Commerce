# Generated by Django 3.2 on 2021-05-10 13:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_alter_auction_createdby'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auction',
            old_name='active',
            new_name='isactive',
        ),
    ]