# Generated by Django 2.2.6 on 2021-11-13 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clientportal', '0008_auto_20210430_1627'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userwallet',
            name='status',
        ),
    ]