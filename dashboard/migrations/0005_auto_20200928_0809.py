# Generated by Django 2.2.6 on 2020-09-28 08:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0004_salesassignment_salesqueue'),
    ]

    operations = [
        migrations.AddField(
            model_name='addsalesnotes',
            name='_u',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='addsalesnotes',
            name='name',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]