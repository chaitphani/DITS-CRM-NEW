from django.urls import (
    re_path, path
)

from . import views

urlpatterns = [
    path('add-commission', views.CommissionCreateAPI.as_view(), name="CommissionCreateAPIView"),
    re_path(r'^check_verified$', views.UserVerifiedAPIView.as_view(), name="UserVerifiedAPIView"),
    re_path(r'^updateload_status$', views.GetUserDocApproveAPIView.as_view(), name="GetUserDocApproveAPIView"),
    re_path(r'^save_country_data$', views.SaveCountryDataAPIView.as_view(), name="SaveCountryDataAPIView"),
    re_path(r'^user_deposit_approval/(?P<user_id>\d+)/(?P<type>\d+)$', views.UsersDepositApproveAPIView.as_view(), name="UsersDepositApproveAPIView"),
    re_path(r'^change_doc_status/(?P<doc_id>\d+)/(?P<value>\d+)$', views.ApproveDisapproveUserDocAPIView.as_view(), name="ApproveDisapproveUserDocAPIView"),
    # re_path(r'^client/r/(?P<client_id>\d+)$', views.GetClientIdRefCampAPIView.as_view(), name="GetClientIdRefCampAPIView"),
    re_path(r'list_securityque$', views.SecurityQueListAPIView.as_view(), name="SecurityQueListAPIView"),
    re_path(r'list_mambers/r/(?P<client_id>\d+)$', views.ClientMamabersListAPIView.as_view(), name="ClientMamabersListAPIView"),
    re_path(r'^user_data/r/$', views.UserRegisterDataListAPIView.as_view(), name="UserRegisterDataListAPIView"),
    re_path(r'^mamber/r/(?P<client_id>\d+)$', views.MamberClientDetailListAPIView.as_view(), name="MamberClientDetailListAPIView"),
    re_path(r'^client_id_member_count/r/(?P<client_id>\d+)$', views.ClientMemberCountListAPIView.as_view(), name="ClientMemberCountListAPIView"),
    re_path(r'^country$', views.CountryListAPIView.as_view(), name="CountryListAPIView"),
    re_path(r'^change_doc_status/(?P<doc_id>\d+)/(?P<value>\d+)$', views.ApproveDisapproveUserDocAPIView.as_view(), name="ApproveDisapproveUserDocAPIView"),
    re_path(r'^get_ib_transaction_history/(?P<client_id>\d+)$', views.IbTransactionAPIView.as_view(), name="get_ib_transaction_history"),
    re_path(r'^get_client_detail/(?P<client_id>\d+)$', views.ClientDetailAPIView.as_view(), name="get_ib_client_detailAPIView"),
    re_path(r'^get_update_client_campaign/(?P<data>[\w|\W]+)$', views.update_client_campaign, name="update_client_campaign_updateAPIView"),
    re_path(r'^get_client_campaign/(?P<username>\w+)$', views.get_client_campaign, name="get_client_campaign"),
    re_path(r'^amount_dashboard$', views.AmountDashboardAPIView.as_view(), name="AmountDashboardAPIView"),
    re_path('^get_register_user_campaign$', views.RegisterUserCampaignListAPIView.as_view(), name="get_register_user_campaign"),

]