# Generated by Django 2.2.6 on 2021-11-13 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientportal', '0009_remove_userwallet_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userwallet',
            name='requested_amount',
        ),
        migrations.DeleteModel(
            name='TradeExperience',
        ),
    ]
