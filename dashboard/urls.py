from django.urls import path,include,re_path
from  . import views


urlpatterns = [
    path('',views.home, name='crm_home'),
    path('client_all_information/<int:client_id>',views.client_all_information,name='client_all_information'),
    path('activity_logs',views.activity_logs, name='activity_logs'),
    path('registration_logs',views.registration_logs, name='registration_logs'),
    path('equity_change_report',views.equity_change_report, name='equity_change_report'),
    path('lead_conversion_report',views.lead_conversion_report, name='lead_conversion_report'),
    path('first_time_deposit_report',views.first_time_deposit_report, name='first_time_deposit_report'),
    path('accounts_approved_report',views.accounts_approved_report, name='accounts_approved_report'),

    path('partner',views.partner, name='partner'),
    path('accounts',views.accounts, name='accounts'),
    path('pendingdeposit',views.PendingDepositTemplateView.as_view(), name='pendingdeposit'),
    path('clientdetailfilter',views.ClientdetailTemplateView.as_view(), name='clientdetailfilter'),
    path('pendingwithdraw',views.pendingwithdraw, name='pendingwithdraw'),
    path('internaltransfer',views.internaltransfer, name='internaltransfer'),
    path('withdraw',views.withdraw, name='withdraw'),
    path('user',views.user, name='user'),
    path('roles',views.roles, name='roles'),
    path('permission',views.permission, name='permission'),
    path('createclient',views.ctclient, name='ctclient'),
    path('createpartner',views.ctpartner, name='ctpartner'),
    path('sale-notes',views.addsalesnotes,name='addsalesnotes'),
    path('sale-notes/<int:sales_id>/edit',views.update_sales_notes,name='edit-sales-note'),
    path('sale-notes/<int:note_id>/delete',views.delete_sales_notes,name='remove-note'),
    path('update_account_type/<int:id>',views.update_account_type,name='update_account_type'),
    path('add_account_type',views.addactype, name='addactype'),
    path('delete_account_type/<int:id>', views.delete_account_type,name="delete_account_type"),
    path('add_currency',views.addcurrency, name='addcurrency'),
    path('update_currency/<int:id>',views.update_currency,name='update_currency'),
    path('delete_currency/<int:id>',views.delete_currency,name="delete_currency"),
    path('addsecurity',views.securityque, name='securityque'),
    path('update_securityque_type/<int:id>,',views.update_securityque_type,name="update_securityque_type"),
    path('delete_securityque_type/<int:id>',views.delete_securityque_type,name="delete_securityque_type"),
    path('access_level',views.access_level, name='access_level'),
    path('update_access_level/<int:id>,',views.update_access_level,name="update_access_level"),
    path('delete_access_level/<int:id>',views.delete_access_level,name="delete_access_level"),
    path('leads_access_level',views.leads_access_level, name='leads_access_level'),
    path('update_leads_access_level/<int:id>,',views.update_leads_access_level,name="update_leads_access_level"),
    path('delete_leads_access_level/<int:id>',views.delete_leads_access_level,name="delete_leads_access_level"),
    path('adddepartment',views.adddepartment,name='adddepartment'),
    path('update_department/<int:id>',views.update_department,name="update_department"),
    path('delete_department/<int:id>',views.delete_department,name="delete_department"),
    path('addoffice',views.addoffice,name='addoffice'),
    path('update_office/<int:id>',views.update_office,name="update_office"),
    path('delete_office/<int:id>',views.delete_office,name="delete_office"),
    path('addbrand',views.addbrand,name="addbrand"),
    path('update_brand/<int:id>',views.update_brand,name="update_brand"),
    path('delete_brand/<int:id>',views.delete_brand,name="delete_brand"),
    path('addleadsregions',views.addleadsregions,name='addleadsregions'),
    path('update_leadsregions/<int:id>',views.update_leadsregions,name="update_leadsregions"),
    path('delete_leadsregions/<int:id>',views.delete_leadsregions,name="delete_leadsregions"),
    path('adddepartment',views.adddepartment,name='adddepartment'),
    # path('user',views.register,name='user'),
    path('login',views.login,name='admin_login'),
    # path('user_documents',views.userdoc,name='user_documents'),
    path('admin_login',views.admin_login,name='admin_login'),
    path('logout',views.admin_logout, name='admin_logout'),
    path('client',views.client, name='client'),
    re_path(r'^clientview/(?P<clientid>\d+)/$', views.clientview, name='clientprofile'),
    path('pendingclients',views.pendingclients, name='pendingclients'),
    path('pendingpartner',views.pendingpartner, name='pendingpartner'),
    path('pendingleverage',views.pendingleverage,name='pendingleverage'),
    # path('notes',views.clientnotes,name='clientnotes'),
    path('demoaccount',views.demoaccount,name='dashdemoaccount'),
    # re_path(r'^demoaccount/(?P<id>\d+)/$', views.demoaccount, name='dashdemoaccount'),
    path('liveaccount',views.liveaccount,name='dashliveaccount'),
    path('dashfinance/<exporttype>',views.finance,name='dashfinance'),
    path('dashfinance',views.finance,name='dashfinance'),
    path('agents',views.agents,name='agents'),
    path('updateagent/<int:id>',views.updateagent,name='updateagent'),
    path('adduser',views.CreateUserTemplateView.as_view(), name='adduser'),
    path('documents/',views.documents,name='documents'),
    # path('mass_mail',views.massmail,name='massmail'),
    path('deposithistory',views.DespositHistoryTemplateView.as_view(),name='deposithistory'),
    path('deposithistory/<exporttype>', views.depositHistoryExport,name='deposithistoryexport'),
    path('withdrawhistory',views.WithdrawHistoryTemplateView.as_view(),name='withdrawhistory'),
    path('withdrawhistory/<exporttype>',views.withdrawHistoryExport,name='withdrawhistoryexport'),
    path('transactionhistory',views.TransactionHistoryTemplateView.as_view(),name='transactionhistory'),
    path('transactionhistory/<exporttype>',views.transactionHistoryExport,name='transactionhistoryexport'),
    path('verify/documents',views.verify_document,name='verify_document'),
    path('unverify/documents/',views.unverify_documents,name='unverify_documents'),
    # path('verify/documents/',views.verify_document,name='verify_document'),
    path('resend_email',views.resend_email,name='resend_email'),
    path('verify/email/<client_id>',views.verify_mail,name='verify_mail'),
    # path('search/id/',views.search_by_id,name='search_by_id'),
    # path('search/name/',views.search_by_name,name='search_by_name'),
    # path('search/email/',views.search_by_email,name='search_by_email'),
    # path('search/mt4/',views.search_by_mt4,name='search_by_mt4'),
    path('add_money_to_wallet/',views.add_money_to_wallet,name='add_money_to_wallet'),
    path('user/history/',views.trans_history,name='trans_history'),
    # path('user/history/<int:client_id>',views.trans_history,name='trans_history'),
    path('user/history/<exporttype>',views.trans_history,name='trans_history'),
    path('withdraw/ib/wallet/money',views.ib_wallet_withdraw_money,name="ib_wallet_withdraw_money"),
    path('user/ib/history/',views.trans_Ibhistory,name='trans_Ibhistory'),
    path('sales_assignment',views.sales_assignment,name='sales_assignment'),
    path('get_sales_notes/<cid>',views.get_sales_notes,name='get_sales_notes'),
    path('client-update/<int:pk>',views.client_update,name='client_update'),
    path('client/<int:pk>/delete',views.client_delete,name='client_delete'),

    #(r'^api/v1/live_accounts/(?P<pk>\d+)/$',views.LiveAccountRetrieve.as_view())
    path('approve/<int:id>/added',views.withdraw_approve,name='withdraw_approve'),
    path('cancel/<int:id>/rejected',views.withdraw_cancel,name='withdraw_cancel'),

    #New urls for new CRM project.....

    # path('trades-data',views.trades_data,name="trades_data"),
    # path('open-trade',views.open_trades_data,name="open_trades_data"),
    # path('deposits-data',views.depo_with_data,name="depo_with_data"),
    # path('clients-data',views.my_client_data,name="my_client_data"),
    # path('json-data',views.JsonData.as_view(),name="json_data"),

    path('agent-data/<int:ref_id>',views.AgentDetailApiView.as_view(),name="agent_details"),

]
