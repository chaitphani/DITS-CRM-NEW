# Generated by Django 2.2.6 on 2021-02-11 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sportapp', '0002_auto_20210210_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='email',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]