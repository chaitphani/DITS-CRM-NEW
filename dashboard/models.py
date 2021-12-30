from django.contrib.auth import default_app_config
from django.db import models
from django.forms.models import model_to_dict, modelformset_factory
from common.models import BaseModel
from django.contrib.auth.models import User
from sportapp.models import Register


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

    choice_field = (('on', 'on'), (False, False))

    user=models.OneToOneField(User,on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    confirmpassword = models.CharField(max_length=100)

    department = models.ForeignKey(Adddepartment, on_delete=models.SET_NULL, null=True)
    office = models.ForeignKey(Addoffice, on_delete=models.SET_NULL, null=True)
    brandvisibility = models.ForeignKey(Addbrand, on_delete=models.SET_NULL, null=True)
    accesslevel = models.ForeignKey(Access_level, on_delete=models.SET_NULL, null=True)
    leadsaccesslevel = models.ForeignKey(Leads_access_level, on_delete=models.SET_NULL, null=True)
    leadsregions = models.ForeignKey(Addleadsregions, on_delete=models.SET_NULL, null=True)
    active_status = models.BooleanField(default=True)
    
    # permissions
    client_edit = models.CharField(max_length=5, choices=choice_field, default=False)
    log_changes_view = models.CharField(max_length=5, choices=choice_field, default=False)
    change_status_compliances = models.CharField(max_length=5, choices=choice_field, default=False)
    note_add = models.CharField(max_length=5, choices=choice_field, default=False)
    note_edit = models.CharField(max_length=5, choices=choice_field, default=False)
    note_delete = models.CharField(max_length=5, choices=choice_field, default=False)
    sales_agent_edit = models.CharField(max_length=5, choices=choice_field, default=False)
    sales_notes_and_follow_ups = models.CharField(max_length=5, choices=choice_field, default=False)
    mt4_demo_account_settings = models.CharField(max_length=5, choices=choice_field, default=False)
    mt4_demo_account_balance_operation = models.CharField(max_length=5, choices=choice_field, default=False)
    mt4_demo_account_changelog = models.CharField(max_length=5, choices=choice_field, default=False)
    mt4_live_account_changelog = models.CharField(max_length=5, choices=choice_field, default=False)
    docs_upload = models.CharField(max_length=5, choices=choice_field, default=False)
    docs_delete = models.CharField(max_length=5, choices=choice_field, default=False)
    pending_clients = models.CharField(max_length=5, choices=choice_field, default=False)
    pending_clients_actions = models.CharField(max_length=5, choices=choice_field, default=False)
    pending_partners = models.CharField(max_length=5, choices=choice_field, default=False)
    pending_partner_actions = models.CharField(max_length=5, choices=choice_field, default=False)
    pending_leverage_change_request = models.CharField(max_length=5, choices=choice_field, default=False)
    view_finances = models.CharField(max_length=5, choices=choice_field, default=False)
    deposit_actions = models.CharField(max_length=5, choices=choice_field, default=False)
    withdrawal_actions = models.CharField(max_length=5, choices=choice_field, default=False)
    lead_add = models.CharField(max_length=5, choices=choice_field, default=False)
    saless_assignment_admin = models.CharField(max_length=5, choices=choice_field, default=False)
    view_management_dashboard = models.CharField(max_length=5, choices=choice_field, default=False)
    accounts_approved = models.CharField(max_length=5, choices=choice_field, default=False)
    equity_change_report = models.CharField(max_length=5, choices=choice_field, default=False)
    first_time_deposits = models.CharField(max_length=5, choices=choice_field, default=False)
    lead_conversion_report = models.CharField(max_length=5, choices=choice_field, default=False)
    
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
