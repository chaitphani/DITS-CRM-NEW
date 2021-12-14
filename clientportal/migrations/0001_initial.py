# Generated by Django 2.2.6 on 2021-12-14 08:45

import clientportal.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sportapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WalletFinance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0)),
                ('t_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='T. Id')),
                ('client_id', models.BigIntegerField(default=0, verbose_name='Client ID')),
                ('type', models.IntegerField(choices=[(0, 'Deposit'), (1, 'Transfer IN'), (2, 'Transfer OUT')], default=0)),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('country', models.CharField(max_length=255, verbose_name='Country')),
                ('t_ip', models.GenericIPAddressField(verbose_name='T. IP')),
                ('t_country', models.CharField(blank=True, max_length=255, null=True, verbose_name='T. Country')),
                ('details', models.CharField(max_length=100)),
                ('amount', models.FloatField(default=0)),
                ('currency', models.CharField(max_length=100)),
                ('feededucted', models.FloatField(blank=True, default=0, null=True)),
                ('status', models.IntegerField(choices=[(0, 'Processed'), (1, 'Not processed')], default=0)),
                ('list_display', models.BooleanField(default=True, verbose_name='Only For Deposit')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='UserWithdraw',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0)),
                ('t_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='T. Id')),
                ('client_id', models.BigIntegerField(default=0, verbose_name='Client ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('country', models.CharField(max_length=255, verbose_name='Country')),
                ('t_ip', models.GenericIPAddressField(verbose_name='T. IP')),
                ('t_country', models.CharField(blank=True, max_length=255, null=True, verbose_name='T. Country')),
                ('details', models.CharField(max_length=100)),
                ('currency', models.CharField(max_length=100)),
                ('amount', models.FloatField()),
                ('username', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('status', models.IntegerField(choices=[(0, 'Pending'), (1, 'Approve'), (2, 'Not Approve')], default=0)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='UserWallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0)),
                ('amount', models.FloatField(default=0)),
                ('w_id', models.BigIntegerField(blank=True, default=0, null=True)),
                ('register', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sportapp.Register')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserDeposits',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0)),
                ('comment', models.TextField(verbose_name='Commnet (Remark)')),
                ('item_id', models.CharField(max_length=255, verbose_name='Item Id')),
                ('batch', models.CharField(blank=True, max_length=255, null=True, verbose_name='Batch Id')),
                ('action_choice', models.IntegerField(choices=[(0, 'Pending'), (1, 'Not Approve'), (2, 'Approve'), (3, 'Try')], default=0)),
                ('walletfinance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clientportal.WalletFinance')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='UserDepositApproval',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approve', models.BooleanField(default=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Uploaddocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0)),
                ('poifront', models.FileField(blank=True, default=None, null=True, upload_to=clientportal.models.user_upload_document)),
                ('poiback', models.FileField(blank=True, default=None, null=True, upload_to=clientportal.models.user_upload_document)),
                ('poafront', models.FileField(blank=True, default=None, null=True, upload_to=clientportal.models.user_upload_document)),
                ('poaback', models.FileField(blank=True, default=None, null=True, upload_to=clientportal.models.user_upload_document)),
                ('crs', models.FileField(blank=True, default=None, null=True, upload_to=clientportal.models.user_upload_document)),
                ('odoc', models.FileField(blank=True, default=None, null=True, upload_to=clientportal.models.user_upload_document)),
                ('type', models.IntegerField(choices=[(1, 'Pending Approval'), (2, 'Approved')], default=1)),
                ('status', models.IntegerField(choices=[(1, 'Not uploaded'), (2, 'Uploaded')], default=1)),
                ('approve', models.BooleanField(default=False)),
                ('date_approved', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LiveAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0)),
                ('account_no', models.BigIntegerField(default=0)),
                ('type', models.SmallIntegerField(default=0, editable=False)),
                ('ac_type', models.CharField(max_length=300)),
                ('cu_type', models.CharField(max_length=300)),
                ('balance', models.FloatField(default=0)),
                ('equity', models.FloatField(blank=True, default=0, null=True)),
                ('group', models.CharField(blank=True, default='', max_length=120, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LiveAcAmount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0)),
                ('amount', models.FloatField(default=0)),
                ('liveaccount', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clientportal.LiveAccount')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DemoAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0)),
                ('account_no', models.BigIntegerField(default=0)),
                ('type', models.SmallIntegerField(default=1, editable=False)),
                ('ac_type', models.CharField(max_length=300)),
                ('cu_type', models.CharField(max_length=300)),
                ('balance', models.FloatField(default=0)),
                ('equity', models.FloatField(blank=True, default=0, null=True)),
                ('group', models.CharField(blank=True, default='', max_length=120, null=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DemoAcAmount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0)),
                ('amount', models.FloatField(default=0)),
                ('demoaccount', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='clientportal.DemoAccount')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Client_Commission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0)),
                ('mt4_account_no', models.BigIntegerField()),
                ('volume', models.FloatField()),
                ('commision_paid', models.FloatField(default=0.0)),
                ('commision_unpaid', models.FloatField(default=0.0)),
                ('wallet', models.FloatField(default=0.0)),
                ('register', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sportapp.Register')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
