from django.contrib import admin
from django.urls import path,include, re_path
from . import views


urlpatterns = [

    path('',views.home, name='home'),
    path('login_client',views.logins, name='login_client'),
    path('logout',views.logout, name='logout'),
    path('code/verification/',views.code_verification,name='code_verification'),
    path('tempapi/<mt4>/', views.tempAPI, name="tempAPI"),

    path('signup',views.UserSignupTemplateView.as_view(), name='signup'),
    path('about',views.about, name='about'),
    path('contact',views.contact, name='contact'),
   
    # re_path(r'^user_verify_link/(?P<user_id>\d+)/(?P<user_token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})$', views.VerifyUserToken.as_view(), name="VerifyUserToken"),
    # path('user_mail_verify',views.user_mail_verify,name="usermailverify"),
    
    path('assets',views.assets,name="assets"),
    path('platform',views.platform,name="platform"),
    path('deposit',views.deposit,name="deposit"),
    path('withdraw',views.withdraw,name="withdraw"),
    path('partner',views.partner,name="partner"),

    path('clients-data',views.clients_data,name="clients_data"),
    # path('payments-data',views.payments_data,name="payments_data"),
    path('transferclient',views.transferClient,name='transferClient'),
    path('trades-data',views.trades_data,name="trades_data"),
    path('assignibtoclient',views.assignIBToClient,name='assignIBToClient'),
    path('dashboard-data',views.getIBAdminAndIBPortalCumulativeData,name='dashboard-data'),
    path('volume-data',views.VolumeCumulativeData,name='volume-data'),
    path('proceed-payout',views.proceed_payout,name='procees-payout'),

]
