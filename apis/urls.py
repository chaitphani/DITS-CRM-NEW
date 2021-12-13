from django.urls import (
    re_path, include, path
)
from . import views

urlpatterns = [
    path('get_registered_user/<int:client_id>/', views.GetRegisteredUser.as_view(), name="GetRegisteredUser"),
    path('update_registered_user/<pk>', views.UpdateRegisteredUser.as_view(), name="UpdateRegisteredUser"),
    re_path(r'^get_account_detail', views.GetAccountDetailAPIView.as_view(), name="GetAccountDetailAPIView"),
    re_path(r'^user_account_data/(?P<account>\d+)$', views.UserAccountOverViewAPIView.as_view(), name="UserAccountOverViewAPIView"),
    re_path(r'^account_edit$', views.AccountEditAPIView.as_view(), name="AccountEditAPIView"),
    re_path(r'^account_pwd_reset$', views.AccountPwdResetView.as_view(), name="AccountPwdResetView"),
    path('live_accounts/<int:user_id>/', views.UserLiveAccountAPIView.as_view(), name="UserLiveAccountAPIView"),
    re_path(r'^store_data$', views.StoreDetailsAPIView.as_view(), name="StoreDetailsAPIView"),
    path('demo_accounts/<int:user_id>/', views.UserDemoAccountAPIView.as_view(), name="UserDemoAccountAPIView"),

    re_path(r'^user_deposit_model$', views.UserWithdrawAPIView.as_view(), name="UserWithdrawAPIView"),

    path('get_camp_users/<ref_id>', views.RegisterUserCampaignView.as_view(), name="get_camp_users"),
    # re_path(r'get_campaign_code/(?P<ib_id>\d+)$', views.get_campaign_code, name='get_campaign_code'),

    # path('live_accounts/<int:user_id>/', views.UserLiveAccountAPIView.as_view(),name='UserLiveAccountAPIView')
]

AUTH_URLS = [
    re_path(r'^auth/', include('apis.auth.urls')),
    re_path(r'^dive_pay_email$', views.UserDepositCheckAPIView.as_view(), name="UserDepositCheckAPIView"),
    re_path(r'^check_user_payment$', views.CheckUserPaymentDivePayAPIView.as_view(), name="CheckUserPaymentDivePayAPIView"),
    re_path(r'^transfer_amount$', views.TransferAmountAPIView.as_view(), name="TransferAmountAPIView"),
    re_path(r'^payment_approve/(?P<user_id>\d+)/(?P<type>\d+)$', views.PaymentApproveDepositAPIView.as_view(), name="PaymentApproveDepositAPIView"),
    re_path(r'^withdraw_approve/(?P<user_id>\d+)/(?P<obj_id>\d+)/(?P<type>\d+)$', views.WithdrawApproveAPIView.as_view(), name="WithdrawApproveAPIView"),
]

urlpatterns += AUTH_URLS
