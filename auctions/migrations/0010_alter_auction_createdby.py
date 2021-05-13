# Generated by Django 3.2 on 2021-05-10 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_user_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='createdby',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='owning', to='auctions.user'),
            preserve_default=False,
        ),
    ]
