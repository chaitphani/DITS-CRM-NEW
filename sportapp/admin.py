from django.contrib import admin

# Register your models here.
from .models import (
    Contact, Profile, Register, Emailtemplate, Profile,RegisterUserCampaign, Mt4trades, Mt4users
)


class RegisterAdmin(admin.ModelAdmin):
   
    list_display = ('fname', 'client_id')
    list_filter = ('country',)


admin.site.register(Contact)
admin.site.register(Mt4trades)
# admin.site.register(Mt4users)
admin.site.register(Register, RegisterAdmin)
admin.site.register(Profile)
admin.site.register(Emailtemplate)
admin.site.register(RegisterUserCampaign)
