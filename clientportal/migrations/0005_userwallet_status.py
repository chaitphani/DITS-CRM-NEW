# Generated by Django 2.2.6 on 2021-04-10 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientportal', '0004_auto_20210119_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='userwallet',
            name='status',
            field=models.CharField(choices=[('A', 'Approved'), ('P', 'Pending')], default='A', max_length=1),
        ),
    ]
