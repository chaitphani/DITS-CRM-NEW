from django.contrib import admin

from . models import *


@admin.register(UserWallet)
class UserWalletModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'register', 'amount')


@admin.register(WalletFinance)
class WalletFinanceModelAdmin(admin.ModelAdmin):
    list_display = ('get_user_id', 'type', 'amount', 'currency', 'feededucted', 'status')

    def get_user_id(self, obj):
        return obj.user.id


admin.site.register(DemoAccount)
admin.site.register(Uploaddocument)
admin.site.register(LiveAccount)
admin.site.register(UserDeposits)
admin.site.register(UserDepositApproval)
admin.site.register(UserWithdraw)
# admin.site.register(TradeExperience)