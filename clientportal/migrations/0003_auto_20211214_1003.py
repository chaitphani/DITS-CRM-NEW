# Generated by Django 2.2.6 on 2021-12-14 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientportal', '0002_auto_20211214_0928'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userwallet',
            name='first_deposit_amount',
        ),
        migrations.RemoveField(
            model_name='userwallet',
            name='first_deposit_date',
        ),
    ]
