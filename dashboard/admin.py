from django.contrib import admin

# Register your models here.
from .models import Securityque,Addaccounttype,SalesQueue,SalesAssignment,Adddepartment,Addoffice,Addleadsregions,Addbrand,Addsalesnotes,Agentusercreate,Comments,Transaction_Method,transaction_ibmethod_mdl,Addcurrency


admin.site.register(Securityque)
admin.site.register(Addaccounttype)
admin.site.register(Adddepartment)
admin.site.register(Addleadsregions)
admin.site.register(Addoffice)
admin.site.register(Addbrand)
admin.site.register(Addsalesnotes)
admin.site.register(Agentusercreate)
admin.site.register(Addcurrency)
admin.site.register(Comments)
admin.site.register(Transaction_Method)
# admin.site.register(Transaction_IbMethod)
admin.site.register(transaction_ibmethod_mdl)
admin.site.register(SalesQueue)
admin.site.register(SalesAssignment)
