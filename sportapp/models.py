from dashboard  .models import *
from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from common.models import BaseModel
from django.dispatch import receiver
# from dashboard.models import Securityque
from .choices import (
    TemplateTypes
)

class Profile(BaseModel):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return "{0} {1}".format(self.user, self.email_confirmed)


class Contact(BaseModel):

    c_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    phone = models.CharField(max_length=70)
    email = models.CharField(max_length=50)
    cmt = models.CharField(max_length=1000)

    def __str__(self):
        return self.lname


class Emailtemplate(BaseModel):

    t_type = models.PositiveIntegerField(default=0, choices=TemplateTypes.CHOICES)
    subject = models.CharField(max_length=100)
    template = models.TextField()

    def __str__(self):
        return "{}".format(self.t_type)


class Register(BaseModel):
   
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    client_id = models.BigIntegerField(default=1001, unique=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    uname = models.CharField(max_length=100)
    dob = models.DateField(max_length=8)
    verify = models.BooleanField(default=False)
    email = models.CharField(max_length=50, unique=True)
    mob = models.CharField(max_length=13)
    pwd1 = models.CharField(max_length=100)
    pwd2 = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address  = models.CharField(max_length=100)
    pincode = models.IntegerField(null=True,blank=True)
    secondaryemail=models.CharField(max_length=100,null=True,blank=True,default=None)
    reasonsecondaryemail=models.CharField(max_length=500,null=True,blank=True)
    city = models.CharField(max_length=50,null=True,blank=True,default=None)
    state  = models.CharField(max_length=100,null=True,blank=True,default=None)
    sque = models.ForeignKey('dashboard.Securityque', null=True,blank=True,default=None, on_delete=models.CASCADE)
    sans = models.CharField(max_length=100,null=True, blank=True)
    client_ib = models.CharField(max_length=100, null=True, blank=True)
    acc_type = models.ManyToManyField('dashboard.Addaccounttype')
    acc_limit = models.IntegerField(default=4)
    demo_acc_limit = models.IntegerField(default=2)
    
    def __str__(self):
        return '{}-{}'.format(self.fname, self.client_id)


class Mt4trades(models.Model):

    ticket = models.IntegerField(primary_key=True)
    login = models.IntegerField()
    symbol = models.CharField(max_length=16)
    digits = models.IntegerField()
    cmd = models.IntegerField()
    volume = models.IntegerField()
    open_time = models.DateTimeField()
    open_price = models.FloatField()
    sl = models.FloatField()
    tp = models.FloatField()
    close_time = models.DateTimeField()
    expiration = models.DateTimeField()
    reason = models.IntegerField()
    conv_rate1 = models.FloatField()
    conv_rate2 = models.FloatField()
    commission = models.FloatField()
    commission_agent = models.FloatField()
    swaps = models.FloatField()
    close_price = models.FloatField()
    profit = models.FloatField()
    taxes = models.FloatField()
    comment = models.CharField(max_length=32)
    internal_id = models.IntegerField()
    margin_rate = models.FloatField()
    timestamp = models.IntegerField()
    magic = models.IntegerField()
    gw_volume = models.IntegerField()
    gw_open_price = models.IntegerField()
    gw_close_price = models.IntegerField()
    modify_time = models.DateTimeField()
    status = models.CharField(max_length=10)

    class Meta:
        db_table = 'MT4_TRADES'

    def __str__(self):
        return '{}'.format(self.login)


class Mt4users(models.Model):
    
    login = models.IntegerField()
    name = models.CharField(max_length=50)
    email = models.CharField(max_length = 50)
    balance = models.FloatField()

    class Meta:
        db_table = "MT4_USERS"

    def __str__(self):
        return str(self.login) + '-' + str(self.name)


class RegisterUserCampaign(BaseModel):
    
    register = models.ForeignKey(Register, on_delete=models.SET_NULL, null=True)
    mt4_id = models.BigIntegerField(default=0)
    ref_code = models.BigIntegerField("Ref Code",default=0,null=True,blank=True) # partner code (ClientPortal User.id)
    campaign_code = models.CharField("Campaign Code", max_length=100,null=True,blank=True,help_text="Campaign Code",)
    campaign = models.CharField("Campaign Name", max_length = 100,null= True,blank = True,help_text="Campaign Name",)
    status = models.IntegerField(default=0)
    
    def __str__(self):
            return '{}-{}'.format(self.register, self.ref_code)


class Addsalesnotes(BaseModel):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(Register, on_delete=models.SET_NULL, null=True)
    note = models.CharField(max_length=1000, null=True, blank=True)
    client_id = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.note