from django.contrib import admin
from django.urls import path,include,re_path
from . import views

urlpatterns = (

    path('performance',views.performance, name='performance'),

    path('',views.dashboard, name='dashboard'),
    path('support',views.support, name='support'),
    path('depositsuccess',views.depositsuccess, name='depositsuccess'),
    path('depositfailure',views.depositfailure, name='depositfailure'),
    path('download_plateform',views.downplat, name='dplateform'),

    path('deposit_by_merchant',views.deposit_by_merchant,name='deposit_by_merchant'),
    path('withdraw_by_merchant',views.withdraw_by_merchant,name='withdraw_by_merchant'),

    path('deposit_client',views.deposit, name='cldeposit'),
    path('deposit_divepay',views.deposit_divepay,name='deposit_divepay'),
    path('deposit_neteller',views.deposit_neteller,name='deposit_neteller'),
    path('deposit_skrill',views.deposit_skrill,name='deposit_skrill'),
    path('manage_funds',views.manage_funds,name='manage_funds'),
    path('withdraw_client',views.withdraw, name='clwithdraw'),
    path('withdraw_divepay',views.withdraw_divepay,name='withdraw_divepay'),
    path('open_liveac',views.laccount, name='liveaccount'),
    path('open_demoac',views.daccount, name='demoaccount'),
    path('changepassword',views.changepassword, name='changepassword'),
    path('profile',views.profile,name='profile'),
    path('addemail',views.addemail,name='addemail'),
    path('address',views.addaddress,name='addaddress'),
    path('live/successful/',views.live_account_response,name='live_account_response'),
    path('demo/successful/',views.demo_account_response,name='live_account_response'),
    path('upload_documents/',views.upload_document,name='upload_document'),
    # path('edit_documents/<int:pk>',views.edit_documents,name='edit_documents'),

    # path('profileupdate',views.profileupdate,name='profileupdate'),
    path('myaccount',views.myaccount,name='myaccount'),
    path('wallet_finance/<exporttype>',views.wallet_finance,name='wallet_finance'),
    path('wallet_finance',views.wallet_finance,name='wallet_finance'),
    path('account_overview',views.account_overview,name='account_overview'),
    path('settings',views.settings,name='settings'),
    path('live_account_detail', views.GetLiveAccountDetailsView.as_view(), name="GetLiveAccountDetailsView"),
    path('demo_account_detail', views.GetDemoAccountDetailsView.as_view(), name="GetDemoAccountDetailsView"),
    path('divepay_success', views.DepositSuccessTemplateView.as_view(), name="DepositSuccessTemplateView"),
    path('divepay_failure', views.DepositFailureTemplateView.as_view(), name="DepositFailureTemplateView"),
     path('bitcoin_payment', views.bitcoin_payment, name="bitcoin_payment"),
    path('usdt', views.usdt, name="usdt"),
    path('user/withdraw/bitcoin', views.bitcoin_withdraw, name="bitcoin_withdraw"),
    path('user/withdraw/usdt', views.usdt_withdraw, name="usdt_withdraw"),
    path('forget-password/',views.forget_password,name='forget_password'),
    path('otp/',views.otp,name='otp'),
    path('reset-password/',views.reset_password,name='reset_password'),
    path('call_edit',views.call_edit,name='call_edit'),
    path('set_language/<language>',views.set_language,name='set_language'),
    # path('mail_test', views.testing_mail),

    path('client_dash',views.client_dash,name='client-dash'),

)