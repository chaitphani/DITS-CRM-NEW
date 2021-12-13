# Generated by Django 2.2.6 on 2021-04-30 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientportal', '0007_tradeexperience'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tradeexperience',
            name='industry',
            field=models.CharField(choices=[('1', 'Financial Services'), ('2', 'Business Administration & Management'), ('3', 'Health care services'), ('4', 'IT'), ('5', 'Other')], default='1', max_length=1),
        ),
    ]