from django.db import models
from common.models import BaseModel
from django.contrib.auth.models import User
from sportapp.models import Register

# Create your models here.

class Securityque(BaseModel):
    name  = models.CharField(max_length=300)

    def __str__(self):
        return self.name

class Addaccounttype(BaseModel):
    name  = models.CharField(max_length=400)

    def __str__(self):
        return self.name

class Addcurrency(BaseModel):
    name  = models.CharField(max_length=400)

    def __str__(self):
        return self.name

class Adddepartment(BaseModel):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Addoffice(BaseModel):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Addbrand(BaseModel):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Addleadsregions(BaseModel):
    name=models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Leads_access_level(BaseModel):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Access_level(BaseModel):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Depositpaymentgetway(BaseModel):
    '''
    type: 0 => Deposit
    type: 1 => Transfer IN
    type: 2 => Transfer OUT
    '''
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    trans_id = models.CharField(max_length=100)
    payment_status = models.CharField(max_length=100)
    fees = models.FloatField()
    amount = models.FloatField()
    type = models.SmallIntegerField(default=0)
    total_amount = models.FloatField()
    currency = models.CharField(max_length=100)
    additional_message = models.CharField(max_length=200)
    member = models.CharField(max_length=100)
    buyer = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    tawkuuid = models.CharField(max_length=500)
    phpsessid = models.CharField(max_length=500)

    def __str__(self):
        return self.member


class Agentusercreate(BaseModel):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    office = models.CharField(max_length=100)
    brandvisibility = models.CharField(max_length=100)
    accesslevel = models.CharField(max_length=100)
    leadsaccesslevel = models.CharField(max_length=100)
    leadsregions = models.CharField(max_length=1000)
    password = models.CharField(max_length=100)
    confirmpassword = models.CharField(max_length=100)

    def __str__(self):
        if self.firstname:
            return self.firstname
        return ""


class Comments(BaseModel):
    name = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return self.name

class Transaction_Method(BaseModel):

    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    type=models.CharField(max_length=100)
    comments=models.ForeignKey('dashboard.Comments',on_delete=models.CASCADE,null=True,blank=True)
    amount=models.FloatField()
    currency=models.ForeignKey('dashboard.Addcurrency',on_delete=models.CASCADE,null=True,blank=True)
    batch_number=models.CharField(max_length=100)
    
    first_deposit_amount = models.FloatField(default=0)
    first_deposit_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ('-id',)


#class Transaction_Ib_Method(BaseModel):
#    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
#    type=models.CharField(max_length=100)
#    comments=models.ForeignKey('dashboard.Comments',on_delete=models.CASCADE,null=True,blank=True)
#    amount=models.FloatField()
#    currency=models.ForeignKey('dashboard.Addcurrency',on_delete=models.CASCADE,null=True,blank=True)
#    batch_number=models.CharField(max_length=100)
#
#    def __str__(self):
#        return self.user.username
#
# class Transaction_IbMethod(BaseModel):
#     id = models.AutoField(primary_key=True)
#     user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
#     client_id = models.BigIntegerField(null=True,blank=True)
#     type=models.CharField(max_length=100)
#     comments=models.ForeignKey('dashboard.Comments',on_delete=models.CASCADE,null=True,blank=True)
#     amount=models.FloatField()
#     currency=models.ForeignKey('dashboard.Addcurrency',on_delete=models.CASCADE,null=True,blank=True)
#     batch_number=models.CharField(max_length=100)
#
#     def __str__(self):
#         return self.user.username



class transaction_ibmethod_mdl(BaseModel):
    id = models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    client_id = models.BigIntegerField(null=True,blank=True)
    type=models.CharField(max_length=100)
    comments=models.ForeignKey('dashboard.Comments',on_delete=models.CASCADE,null=True,blank=True)
    amount=models.FloatField()
    currency=models.ForeignKey('dashboard.Addcurrency',on_delete=models.CASCADE,null=True,blank=True)
    batch_number=models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class SalesQueue(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class SalesAssignment(BaseModel):
    agent = models.OneToOneField(Agentusercreate, on_delete=models.CASCADE)
    enabled_state = models.BooleanField(null=True, blank=True)
    default_state = models.BooleanField(null=True, blank=True)
    country_list = models.CharField(max_length=255, null=True, blank=True)
    sales_queues = models.ForeignKey(SalesQueue, on_delete=models.CASCADE, null=True, blank=True)
    promo_code = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.agent.firstname
