from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django .urls import reverse
from dashboard.views import exportData
from dashboard.models import Addaccounttype
from dashboard.models import Addcurrency
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import View, TemplateView
from django.conf import settings
from django.http import HttpResponse
from .models import DemoAccount,UserWithdraw
from .models import LiveAccount
from django.shortcuts import get_object_or_404
from .models import Uploaddocument,WalletFinance
from django.contrib import auth
from django.core.mail import send_mail
import datetime
from django . core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password
from sportapp.models import Register, RegisterUserCampaign
from dashboard.models import Transaction_Method
import random, string
from clientportal import jwt_decode
from .jwt_decode import (
    encode_jwt, decode_jwt
)
from django.db import connection
from dashboard.filters import DateRangeMaker
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from django.db.models import Sum

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from . form import *
from django.utils import translation
import random
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt


def edit_mt4_account_api_call(request_data):
    url = 'https://demodc.use.6i.nullpoint.io/accountedit/'
    jwt_dict_data = jwt_decode.edit_account
    jwt_dict_data['account'] = request_data['account']
    # jwt_dict_data['comment'] = "{0},{1}".format(
    #          request_data['campaignCode'],
    #          request_data['ibId']
    #     )
    encoded_return_data = "request_message={0}".format(jwt_decode.encode_jwt(data=jwt_dict_data))
    response_api = requests.post(url, data=encoded_return_data, verify=False)
    return {"data": jwt_decode.decode_jwt(data=response_api.text)}


from datetime import datetime, date
@login_required(login_url='login_client')
def client_dash(request):

    today = date.today()
    context = {}
    free_margin, logins, profit_list, list_flat, graph_list, set_list = [], [], [], [], [], []
    open_pro_list, flat_list, profitability_list, final_list, final_list_2 = [], [], [], [], []
    cls_comm_list, cls_comm_sum_list, comm_trades_list, open_com_lst = [], [], [], []
    swaps_in_cls, cls_swap_lst, swaps_in_opn = [], [], []

#############  for margin free #########

    _data = f'https://crm.divsolution.com/api/v1/live_accounts/{request.user.id}/'
    get_data = requests.get(_data).json()
    for data in get_data['data']:
        try:
            if data['login']:
                logins.append(data['login'])
                free_margin.append(data['margin_free'])
        except:
            pass

    for i in range(0, len(free_margin)):
        free_margin[i] = float(free_margin[i])

    context['free_margin'] = round(sum(free_margin), 2)

#############  margin free ends  #########

    with connection.cursor() as cursor:
        for log in logins:
            cursor.execute(f"select MT4_TRADES.PROFIT from(MT4_TRADES join MT4_USERS on MT4_TRADES.LOGIN=MT4_USERS.LOGIN) join MT4_GROUPS on MT4_GROUPS.GROUP=MT4_USERS.GROUP where MT4_TRADES.LOGIN like '%{log}%' and MT4_TRADES.COMMENT = '' and DATE_FORMAT(MT4_TRADES.CLOSE_TIME, '%Y-%m-%d') like '%{today}%' and MT4_GROUPS.COMPANY like '%Henan Xinluan Information%'")
            data_sql = cursor.fetchall()

            for data in data_sql:
                data_list = list(data)
                profit_list.append(data_list)
                
            cursor.execute(f"select MT4_TRADES.COMMISSION from(MT4_TRADES join MT4_USERS on MT4_TRADES.LOGIN=MT4_USERS.LOGIN) join MT4_GROUPS on MT4_GROUPS.GROUP=MT4_USERS.GROUP where MT4_TRADES.LOGIN like '%{log}%' and MT4_TRADES.COMMENT = '' and DATE_FORMAT(MT4_TRADES.CLOSE_TIME, '%Y-%m-%d') like '%{today}%' and MT4_GROUPS.COMPANY like '%Henan Xinluan Information%'")
            close_comm = cursor.fetchall()
            for comm in close_comm:
                cls_comm_lis = list(comm)
                cls_comm_list.append(cls_comm_lis)
            
            cursor.execute(f"select MT4_TRADES.SWAPS from(MT4_TRADES join MT4_USERS on MT4_TRADES.LOGIN=MT4_USERS.LOGIN) join MT4_GROUPS on MT4_GROUPS.GROUP=MT4_USERS.GROUP where MT4_TRADES.LOGIN like '%{log}%' and MT4_TRADES.COMMENT = '' and DATE_FORMAT(MT4_TRADES.CLOSE_TIME, '%Y-%m-%d') like '%{today}%' and MT4_GROUPS.COMPANY like '%Henan Xinluan Information%'")
            cls_swaps = cursor.fetchall()
            for swaps in cls_swaps:
                cls_swaps_list = list(swaps)
                swaps_in_cls.append(cls_swaps_list)

            cursor.execute(f"select MT4_TRADES.SYMBOL from(MT4_TRADES join MT4_USERS on MT4_TRADES.LOGIN=MT4_USERS.LOGIN) join MT4_GROUPS on MT4_GROUPS.GROUP=MT4_USERS.GROUP where MT4_TRADES.LOGIN like '%{log}%' and MT4_TRADES.COMMENT = '' and MT4_TRADES.CLOSE_TIME = '1970-01-01 00:00:00' and MT4_GROUPS.COMPANY like '%Henan Xinluan Information%'")
            graph_response = cursor.fetchall()

            for response in graph_response:
                for graph in response:
                    graph_list.append(graph)

            cursor.execute(f"select MT4_TRADES.PROFIT from(MT4_TRADES join MT4_USERS on MT4_TRADES.LOGIN=MT4_USERS.LOGIN) join MT4_GROUPS on MT4_USERS.GROUP=MT4_GROUPS.GROUP where MT4_TRADES.LOGIN like '%{log}%' and MT4_TRADES.COMMENT = '' and MT4_TRADES.CLOSE_TIME = '1970-01-01 00:00:00' and MT4_GROUPS.COMPANY like '%Henan Xinluan Information%' ")
            open_pro = cursor.fetchall()

            for pro in open_pro:
                pro_list = list(pro)
                open_pro_list.append(pro_list)

            cursor.execute(f"select MT4_TRADES.COMMISSION from(MT4_TRADES join MT4_USERS on MT4_TRADES.LOGIN=MT4_USERS.LOGIN) join MT4_GROUPS on MT4_USERS.GROUP=MT4_GROUPS.GROUP where MT4_TRADES.LOGIN like '%{log}%' and MT4_TRADES.COMMENT = '' and MT4_TRADES.CLOSE_TIME = '1970-01-01 00:00:00' and MT4_GROUPS.COMPANY like '%Henan Xinluan Information%' ")
            open_comm_pro = cursor.fetchall()

            for open_comm in open_comm_pro:
                open_comm_list = list(open_comm)
                open_com_lst.append(open_comm_list)
            
            cursor.execute(f"select MT4_TRADES.SWAPS from(MT4_TRADES join MT4_USERS on MT4_TRADES.LOGIN=MT4_USERS.LOGIN) join MT4_GROUPS on MT4_USERS.GROUP=MT4_GROUPS.GROUP where MT4_TRADES.LOGIN like '%{log}%' and MT4_TRADES.COMMENT = '' and MT4_TRADES.CLOSE_TIME = '1970-01-01 00:00:00' and MT4_GROUPS.COMPANY like '%Henan Xinluan Information%' ")
            opn_swaps = cursor.fetchall()

            for swaps in opn_swaps:
                opn_swaps_list = list(swaps)
                swaps_in_opn.append(opn_swaps_list)

            cursor.execute(f"select MT4_TRADES.PROFIT from(MT4_TRADES join MT4_USERS on MT4_TRADES.LOGIN=MT4_USERS.LOGIN) join MT4_GROUPS on MT4_GROUPS.GROUP=MT4_USERS.GROUP where MT4_TRADES.LOGIN like '%{log}%' and MT4_TRADES.COMMENT = '' and MT4_GROUPS.COMPANY like '%Henan Xinluan Information%'")
            proftablity_data = cursor.fetchall()

            for ability in proftablity_data:
                lists_data = list(ability)
                profitability_list.append(lists_data)
    
#############  for closing p&l ###########

    # for i in range(len(profit_list)):
    #     for j in range(len(profit_list[i])):
    #         list_flat.append(profit_list[i][j])
    list_flat = [tis for pros in profit_list for tis in pros]

    cls_comm_sum_list = [sit for pros in cls_comm_list for sit in pros]

    cls_swap_lst = [ist for pros in swaps_in_cls for ist in pros]

    pl_with_comm = sum(cls_comm_sum_list)+sum(list_flat)+sum(cls_swap_lst)

############# closing p&l ends ###########

#############  for profitability ###########

    final_list = [tem for em in profitability_list for tem in em]
    final_list_2 = [pro for pro in final_list if pro > 0]

############# profitability ends ###########

#############  for open p&l ###########

    flat_list = [item for open_pro in open_pro_list for item in open_pro]

    final_flat_list = [item for open_pro in open_com_lst for item in open_pro]

    final_swpas_list = [item for open_pro in swaps_in_opn for item in open_pro]

    open_comm_with_pl = sum(final_flat_list)+sum(flat_list)+sum(final_swpas_list)

############# open p&l ends ###########

############# Graph data starts ###########

    for crypto in graph_list:
        graph_list.count(crypto)
        set_list.extend([crypto, graph_list.count(crypto)])

    res_dct = {set_list[i]: set_list[i + 1] for i in range(0, len(set_list), 2)}
    key_data, values_data, values_graph_data, list_graph_val = [], [], [], []

    for key, value in res_dct.items():
        key = key.replace('-','')
        key_data.append(key)
        values_data.append(value)

    for values in values_data:
        values_to_append = round((values/sum(values_data))*100, 2)
        values_graph_data.append(values_to_append)

    if profit_list and cls_comm_sum_list:
        context['closing_p_l'] = round(pl_with_comm, 2)
    else:
        pass

    if open_pro_list and open_com_lst:
        context['open_p_l'] = round(open_comm_with_pl, 2)
    else:
        pass

    if profitability_list:
        context['profitability'] = round((len(final_list_2)/len(profitability_list))*100, 2)
    else:
        pass
    
    context['values_graph_data'] = values_graph_data
    context['key_data'] = key_data

############# Graph data ends ###########

    return render(request, 'clientportal/dashboard.html', context=context)

    
def call_edit(request):
    data = {
    "account":'8000048',
    "campaignCode":'ITj[2q0^',
    "ibId":'10001'
    }
    edit_mt4_account_api_call(data)
    return JsonResponse({'message':'done'})


def set_language(request, language):
    old_lang = translation.get_language()
    translation.activate(language)
    return redirect('/clientportal', lang=language)


def make_password(stringLength=15):
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(password_characters) for i in range(stringLength))


@login_required(login_url='login_client')
def dashboard(request):

    live_acounts = LiveAccount.objects.filter(user=request.user)
    demo_acounts = DemoAccount.objects.filter(user=request.user)
    
    return render(request,'clientportal/client_index.html', {'lives':live_acounts, 'demos':demo_acounts})
    # return render(request,'clientportal/client_index.html')


@login_required(login_url='login_client')
def profile(request, lang=None):

    # admin_user = User.objects.all().filter(is_superuser=True)[0]
    register = Register.objects.filter(user_id=request.user.id)
    year_val = ''
    month_val = ''
    date_val = ''
    dob_year = ''
    dob_month = ''
    dob_date = ''
    secondary_email_val = ''

    for i in register:
        date_split = str(i.added_on).split(' ')[0]
        year_val = date_split.split('-')[0]
        month_val = date_split.split('-')[1]
        date_val = date_split.split('-')[2]
        dob_datesplit = str(i.dob).split('-')
        dob_year = dob_datesplit[0]
        dob_month = dob_datesplit[1]
        dob_date = dob_datesplit[2]

        if i.secondaryemail == None:
            secondary_email_val = 'No Email'
        else:
            secondary_email_val = i.secondaryemail
    return render(request, 'clientportal/profile.html', {
        'r': register,
        'added_on_year_val': year_val,
        'added_on_month_val': month_val,
        'added_on_date_val': date_val,
        'secondary_email_val': secondary_email_val,
        'dob_year':dob_year,
        'dob_month':dob_month,
        'dob_date':dob_date,
        })


@login_required(login_url='login_client')
def wallet_finance(request, exporttype=None):
    
    wallet = WalletFinance.objects.filter(list_display=True, user_id=request.user.id).order_by('-id')
    transaction = Transaction_Method.objects.filter(user_id=request.user.id).order_by('-id')

    response_list = []

    year_val = ''
    month_val = ''
    date_val = ''
    id = ''
    type = ''
    amount = ''
    currency = ''
    comments = ''
    status = ''
    transfer_to = ''
    transfer_in = ''
    transfer_type = ''
    get_status_display = ''

    if not request.GET.get('added_on'):
        for i in transaction:
            date_split = str(i.added_on).split(' ')[0]
            year_val = date_split.split('-')[0]
            month_val = date_split.split('-')[1]
            date_val = date_split.split('-')[2]
            id = i.id
            t = i.type
            amount = i.amount
            currency = i.currency
            comments = i.comments.name
            if comments == "Virtual currency":
                currency_type = "Crypto"
            else:
                currency_type = "USDT"
            if t == '1':
                transfer_type = "Deposit"
            else:
                transfer_type = "Withdrawal"
            response_list.append((year_val+month_val+date_val, {
                'added_on_year_val': year_val,
                'added_on_month_val': month_val,
                'added_on_date_val': date_val,
                'id':id,
                'added_on':i.added_on,
                'transfer_type':transfer_type,
                'currency':"usd",
                'comments':comments,
                'amount':amount,
                'get_status_display':"Completed"
            }))

        for i in wallet:

            date_split = str(i.added_on).split(' ')[0]
            year_val = date_split.split('-')[0]
            month_val = date_split.split('-')[1]
            date_val = date_split.split('-')[2]
            if i.type == 1:
                transfer_type = 'Deposit'
                type = 'Transfer IN'
            elif i.type == 2:
                transfer_type = 'Withdrawal'
                type = 'Transfer OUT'

            if i.details.startswith('Transfer from'):
                transfer_to = i.details.replace('Transfer from','')
            elif i.details.startswith('Transfer to'):
                transfer_to = i.details.replace('Transfer to','')
            elif i.details.startswith('Transfer Out'):
                transfer_to = i.details.replace('Transfer Out','')
            elif i.details.startswith('Transfer IN'):
                transfer_to = i.details.replace('Transfer IN','')
            if i.status == 0:
                get_status_display = 'Completed'
            elif  i.status == 1:
                get_status_display = 'Not Processed'
            if i.currency == 'USD':
                currency = 'usd'

            response_list.append((year_val+month_val+date_val, {
                'wallet':wallet,
                'amount':round(i.amount, 2),
                'type':type,
                'added_on':i.added_on,
                'currency':currency.upper(),
                'get_status_display':get_status_display,
                'added_on_year_val': year_val,
                'added_on_month_val': month_val,
                'added_on_date_val': date_val,
                'transfer_to':transfer_to,
                'transfer_type':transfer_type
            }))

    elif request.GET.get('added_on') and int(request.GET.get('added_on')) != 7:
        d= DateRangeMaker()
        value = d.change(int(request.GET.get('added_on')))
        transaction = transaction.filter(added_on__range=[value, d.today_date_obj.strftime('%Y-%m-%d')])
        for i in transaction:
            date_split = str(i.added_on).split(' ')[0]
            year_val = date_split.split('-')[0]
            month_val = date_split.split('-')[1]
            date_val = date_split.split('-')[2]
            id = i.id
            t = i.type
            amount = i.amount
            currency = i.currency
            comments = i.comments.name
            if comments == "Virtual currency":
                currency_type = "Crypto"
            else:
                currency_type = "USDT"
            if t == '1':
                transfer_type = "Deposit"
            else:
                transfer_type = "Withdrawal"
            response_list.append((year_val+month_val+date_val, {
                'added_on_year_val': year_val,
                'added_on_month_val': month_val,
                'added_on_date_val': date_val,
                'id':id,
                'added_on':i.added_on,
                'transfer_type':transfer_type,
                'currency':"usd",
                'comments':comments,
                'amount':amount,
                'get_status_display':"Completed"
            }))

        for i in wallet:
            date_split = str(i.added_on).split(' ')[0]
            year_val = date_split.split('-')[0]
            month_val = date_split.split('-')[1]
            date_val = date_split.split('-')[2]
            if i.type == 1:
                transfer_type = 'Deposit'
                type = 'Transfer IN'
            elif i.type == 2:
                transfer_type = 'Withdrawal'
                type = 'Transfer OUT'

            if i.details.startswith('Transfer from'):
                transfer_to = i.details.replace('Transfer from','')
            elif i.details.startswith('Transfer to'):
                transfer_to = i.details.replace('Transfer to','')
            elif i.details.startswith('Transfer Out'):
                transfer_to = i.details.replace('Transfer Out','')
            elif i.details.startswith('Transfer IN'):
                transfer_to = i.details.replace('Transfer IN','')
            if i.status == 0:
                get_status_display = 'Completed'
            elif  i.status == 1:
                get_status_display = 'Not Processed'
            if i.currency == 'USD':
                currency = 'usd'

            response_list.append((year_val+month_val+date_val, {
                'wallet':wallet,
                'amount':round(i.amount, 2),
                'type':type,
                'added_on':i.added_on,
                'currency':currency.upper(),
                'get_status_display':get_status_display,
                'added_on_year_val': year_val,
                'added_on_month_val': month_val,
                'added_on_date_val': date_val,
                'transfer_to':transfer_to,
                'transfer_type':transfer_type
            }))
    
    elif request.GET.get('added_on') and int(request.GET.get('added_on')) == 7:

        transaction = transaction.filter(added_on__range=[request.GET.get('startDate'), request.GET.get('endDate')])
        for i in transaction:
            date_split = str(i.added_on).split(' ')[0]
            year_val = date_split.split('-')[0]
            month_val = date_split.split('-')[1]
            date_val = date_split.split('-')[2]
            id = i.id
            t = i.type
            amount = i.amount
            currency = i.currency
            comments = i.comments.name
            if comments == "Virtual currency":
                currency_type = "Crypto"
            else:
                currency_type = "USDT"
            if t == '1':
                transfer_type = "Deposit"
            else:
                transfer_type = "Withdrawal"
            response_list.append((year_val+month_val+date_val, {
                'added_on_year_val': year_val,
                'added_on_month_val': month_val,
                'added_on_date_val': date_val,
                'id':id,
                'transfer_type':transfer_type,
                'currency':"usd",
                'comments':comments,
                'added_on':i.added_on,
                'amount':amount,
                'get_status_display':"Completed"
            }))

        for i in wallet:
            date_split = str(i.added_on).split(' ')[0]
            year_val = date_split.split('-')[0]
            month_val = date_split.split('-')[1]
            date_val = date_split.split('-')[2]
            if i.type == 1:
                transfer_type = 'Deposit'
                type = 'Transfer IN'
            elif i.type == 2:
                transfer_type = 'Withdrawal'
                type = 'Transfer OUT'

            if i.details.startswith('Transfer from'):
                transfer_to = i.details.replace('Transfer from','')
            elif i.details.startswith('Transfer to'):
                transfer_to = i.details.replace('Transfer to','')
            elif i.details.startswith('Transfer Out'):
                transfer_to = i.details.replace('Transfer Out','')
            elif i.details.startswith('Transfer IN'):
                transfer_to = i.details.replace('Transfer IN','')
            if i.status == 0:
                get_status_display = 'Completed'
            elif  i.status == 1:
                get_status_display = 'Not Processed'
            if i.currency == 'USD':
                currency = 'usd'

            response_list.append((year_val+month_val+date_val, {
                'wallet':wallet,
                'amount':round(i.amount, 2),
                'type':type,
                'added_on':i.added_on,
                'currency':currency.upper(),
                'get_status_display':get_status_display,
                'added_on_year_val': year_val,
                'added_on_month_val': month_val,
                'added_on_date_val': date_val,
                'transfer_to':transfer_to,
                'transfer_type':transfer_type
            }))
    response_data = [d[1] for d in sorted(response_list, key=lambda x:x[0])]
    if exporttype:
        response_list = []
        title_headers = ["Date", "Description", "Amount", "Currency", "Status"]
        for rd in response_data:
            dt = f"{rd['added_on_date_val']}-{rd['added_on_month_val']}-{rd['added_on_year_val']}"
            if rd.get('type'):
                details = f"{rd['transfer_type']}-{rd['transfer_to']}"
            else:
                details = f"{rd['transfer_type']}-{rd['comments']}"
            amt = rd['amount']
            curr = rd['currency']
            status = rd['get_status_display']
            response_list.append([dt, details, amt, curr, status])
        return exportData(response_list, exporttype, 'finance', title_headers)
    else:
        return render(request, 'clientportal/walletfinance.html',{
            'response_list':response_data
        })


def get_object_or_none(Models, request):
    try:
        obj = Models.objects.get(user=request.user)
        return obj
    except Models.DoesNotExist:
        return None


@login_required(login_url='login_client')
def upload_document(request):
    documents = get_object_or_none(Uploaddocument, request)
    if not documents:
        if request.method == 'POST':
            docs = Uploaddocument.objects.create(
                user=request.user,
                poifront=request.FILES.get('pidentityfront'),
                poiback=request.FILES.get('pidentityback'),
                poafront=request.FILES.get('paddressfront'),
                poaback=request.FILES.get('paddressback'),
                crs=request.FILES.get('crscans'),
                odoc=request.FILES.get('otherdoc')
            )
            docs.status=2
            docs.save()
            # return redirect('dashboard')
        return render(request,'clientportal/edit_document.html',{'documents':documents})
    else:
        user_doc = get_object_or_404(Uploaddocument,user=request.user)
        if request.method == 'POST':
            if request.FILES.get('pidentityfront'):
                user_doc.poifront = request.FILES.get('pidentityfront')
            if request.FILES.get('pidentityback'):
                user_doc.poiback = request.FILES.get('pidentityback')
            if request.FILES.get('paddressfront'):
                user_doc.poafront = request.FILES.get('paddressfront')
            if request.FILES.get('paddressback'):
                user_doc.poaback = request.FILES.get('paddressback')
            if request.FILES.get('crscans'):
                user_doc.crs = request.FILES.get('crscans')
            if request.FILES.get('otherdoc'):
                user_doc.odoc = request.FILES.get('otherdoc')
            user_doc.status=2
            user_doc.save()
            # return redirect('profile')
        return render(request,'clientportal/edit_document.html',{'user_doc':user_doc,'documents':documents})


def forget_password(request):

    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
        except:
            user = False
        if user:
            request.session['email'] = user.email
            request.session['username'] = user.username
            otp = random.randint(10000, 99999)
            print("OTP----------------for reset password", otp)
            request.session['otp'] = otp
            request.session.set_expiry(5*60)
            subject = 'OTP Requested for forgotten password'
            message = "We received a forgot password request from your account.\nMake sure not to share your OTP with anyone.\n OTP :{}.\n\n\nplease verify your account if it's not you".format(str(otp))
            from_email = 'info@divsolution.com'
            send_mail(subject, message, from_email,
                      [email], fail_silently=False)
            return redirect('otp')
        else:
            messages.error(request, 'Enter a valid Registered Email..!')
            message = 'Enter a valid Registered Email..!'

    return render(request,'clientportal/forget_password.html')


def otp(request):

    session_otp = request.session.get('otp')

    if request.method == 'POST':
        otp = request.POST['otp']
        if int(session_otp) == int(otp):
            return redirect('reset_password')
            del request.session['otp']
        else:
            messages.error(request, 'Invalid OTP, try again')
    return render(request, 'clientportal/otp.html')


def reset_password(request):

    try:
        rocks12 = User.objects.get(email=request.session['email'])
    except:
        # messages.error(request, 'Your session timed out....!')
        response = '<script>alert("Your session times out...!");window.location.replace("https://crm.divsolution.com/login_client")</script>'
        return HttpResponse(response)

    if request.method == 'POST':
        email = rocks12.email
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            rocks12.set_password(password)
            rocks12.save()
            subject = request.session['username'].capitalize(
            ) + "Your Password reset"
            message = 'Please find your account details below with credentials after password reset \nEmail :{}\nUser Name :{}\nPassword :{}'.format(
                email.lower(), request.session['username'], str(password))
            from_email = 'ditstaskmanager@gmail.com'
            send_mail(
                subject,
                message,
                from_email,
                [email],
                fail_silently=False,
            )
            return redirect('login_client')
            del request.session['username']
        else:
            messages.error(request, 'passwords mis-match')

    return render(request,'clientportal/reset_password.html')


def changepassword(request):

    message = None
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        currentpassword = request.user.password  # user's current password
        form = PasswordChangeForm(user=request.user, data=request.POST)
        currentpasswordentered = request.POST.get('old_password')
        newpasswordentered = request.POST.get('new_password1')
        oldpasswordcheck = check_password(
            currentpasswordentered, currentpassword)
        if oldpasswordcheck:
            if newpasswordentered != currentpasswordentered:
                if form.is_valid():
                    form.save()
                    message = 'The password has been changed successfully'
                    return redirect('login_client')
                else:
                    print(form.errors)
            else:
                message = 'The passwords can not be same as the old one.'
        else:
            message = 'The old password that you enter is wrong.'
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request,'clientportal/changepassword.html',{'message': message, 'form': form})


def logins(request):

    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['pwd']
        register = auth.authenticate(username=username, password=password)
        if register is not None:
            auth.login(request,register)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error':'Invalid Login Credentials'})
    else:
        context_data={
            'u':User.objects.all()
        }
        return render(request, 'login.html', context_data)


@login_required(login_url='login_client')
def myaccount(request):
    return render(request,'clientportal/myaccount.html')


class DepositSuccessTemplateView(TemplateView):
    template_name = "clientportal/depositsuccess.html"

class DepositFailureTemplateView(TemplateView):
    template_name = "clientportal/depositfailure.html"


import ast
@login_required(login_url='login_client')
def account_overview(request):

    context = {}
    duration = ''
    sell_max = ''
    buy_max = ''
    sell_min = ''
    buy_min = ''
    avg_win = ''
    avg_loss = ''
    worst_trade_value = ''
    best_trade_value = ''
    response_list, vol_list, profit_list, withdraw_list, deposit_list = [], [], [], [], []
    gp_list, gl_list, close_tme, open_tme = [], [], [], []
    buy_points_list, sell_point_list, profit_trades_list, loss_trades_list = [], [], [], []
    avg_pro_list, avg_loss_list, open_posit_list = [], [], []
    profttradesinsell, profttradesinbuy, best_worst_trade, all_list, graph_list = [], [], [], [], []

    account_no = request.GET.get('account')
    with connection.cursor() as cursor:
        cursor.execute(f"select MT4_TRADES.VOLUME, MT4_TRADES.PROFIT, MT4_TRADES.OPEN_TIME, MT4_TRADES.CLOSE_TIME, MT4_TRADES.TICKET, MT4_TRADES.SYMBOL, MT4_TRADES.OPEN_PRICE, MT4_TRADES.CLOSE_PRICE, MT4_TRADES.COMMISSION, MT4_TRADES.SWAPS, MT4_TRADES.CMD from (MT4_TRADES join MT4_USERS on MT4_TRADES.LOGIN=MT4_USERS.LOGIN) join MT4_GROUPS on MT4_USERS.GROUP=MT4_GROUPS.GROUP where MT4_TRADES.LOGIN like '%{account_no}%' and MT4_TRADES.COMMENT = '' and MT4_GROUPS.COMPANY like '%Henan Xinluan Information%'")
        data_sql = cursor.fetchall()
        
        # 1-volume, 2-profit, 3-open_time, 4-close_time, 5-ticket, 6-symbol, 7-open_price, 8-close_price, 9-commission, 10-swaps, 11-cmd

        for data in data_sql:
            print('------data sql--------', data)
            data_list = list(data)
            all_list.append(data)
            vol_list.append(data_list[0])
            profit_list.append(data_list[1])

            open_tme.append(data_list[2])
            close_tme.append(data_list[3])

            gross_values = data_list[1]
            if str(gross_values).startswith('-'):
                values = str(gross_values).replace("-", "")
                gl_list.append(float(values))
            else:
                gp_list.append(gross_values)

        for pro in profit_list:
            if pro > 0:
                profit_trades_list.append(pro)
            else:
                loss_trades_list.append(pro)

        gross_profit = sum(gp_list)
        gross_loss = sum(gl_list)
        if gross_profit:
            profit_factor = round((gross_profit/gross_loss), 2)
        else:
            profit_factor = 0

        if close_tme:
            if close_tme[-1] >= open_tme[-1]:
                duration = close_tme[-1] - open_tme[-1]
            else:
                duration = 0
        else:
            pass
# -------------

        cursor.execute(f"select MT4_TRADES.VOLUME, MT4_TRADES.PROFIT, MT4_TRADES.OPEN_TIME, MT4_TRADES.CLOSE_TIME, MT4_TRADES.TICKET, MT4_TRADES.SYMBOL, MT4_TRADES.OPEN_PRICE, MT4_TRADES.CLOSE_PRICE, MT4_TRADES.COMMISSION, MT4_TRADES.SWAPS, MT4_TRADES.CMD from (MT4_TRADES join MT4_USERS ON MT4_TRADES.LOGIN=MT4_USERS.LOGIN) JOIN MT4_GROUPS ON MT4_USERS.GROUP=MT4_GROUPS.GROUP where MT4_TRADES.LOGIN like '%{account_no}%' and MT4_TRADES.COMMENT = '' and MT4_TRADES.CLOSE_TIME = '1970-01-01 00:00:00' and MT4_GROUPS.COMPANY like '%Henan Xinluan Information%'")
        open_positions_data = cursor.fetchall()

        for open_positions in open_positions_data:
            position_list = list(open_positions)
            open_posit_list.append(position_list)

# -------------
        cursor.execute(f"select MT4_TRADES.SYMBOL from (MT4_TRADES join MT4_USERS ON MT4_TRADES.LOGIN=MT4_USERS.LOGIN) join MT4_GROUPS ON MT4_USERS.GROUP=MT4_GROUPS.GROUP where MT4_TRADES.LOGIN like '%{account_no}%' and MT4_TRADES.COMMENT = '' and MT4_GROUPS.COMPANY like '%Henan Xinluan Information%' ")

        graph_response = cursor.fetchall()
        for response in graph_response:
            for graph in response:
                graph_list.append(graph)
        set_list = []
        for crypto in graph_list:
            graph_list.count(crypto)
            set_list.extend([crypto, graph_list.count(crypto)])

        res_dct = {set_list[i]: set_list[i + 1] for i in range(0, len(set_list), 2)}
        key_data = []
        values_data = []
        values_graph_data = []
        list_graph_val = []
        for key, value in res_dct.items():
            key_data.append(key)
            values_data.append(value)
        for values in values_data:
            values_graph_data.append((values/len(values_data))*100)
            # list_graph_val.append((values/len(values_data))*100)

        cursor.execute(f"select MT4_TRADES.PROFIT, MT4_TRADES.SYMBOL, MT4_TRADES.OPEN_PRICE, MT4_TRADES.CLOSE_PRICE from (MT4_TRADES join MT4_USERS ON MT4_TRADES.LOGIN=MT4_USERS.LOGIN) join MT4_GROUPS on MT4_USERS.GROUP=MT4_GROUPS.GROUP where MT4_TRADES.LOGIN like '%{account_no}%' and MT4_TRADES.COMMENT = '' and MT4_GROUPS.COMPANY like '%Henan Xinluan Information%' ")

        average_points_data = cursor.fetchall()
        for average in list(average_points_data):
            if str(average[0]).startswith('-'):
                if average[1].startswith('X'):
                    avg_loss = (average[2]-average[3])*100
                else:
                    avg_loss = (average[2]-average[3])*100000
                avg_loss_list.append(avg_loss)
            else:
                if average[1].startswith('X'):
                    avg_pro = (average[2]-average[3])*100
                else:
                    avg_pro = (average[2]-average[3])*100000
                avg_pro_list.append(avg_pro)

        if profit_trades_list:
            avg_win = sum(avg_pro_list)/len(profit_trades_list)
        else:
            pass

        if loss_trades_list:
            avg_loss = sum(avg_loss_list)/len(loss_trades_list)
        else:
            pass

        cursor.execute(f"select MT4_TRADES.VOLUME, MT4_TRADES.PROFIT, MT4_TRADES.OPEN_TIME, MT4_TRADES.CLOSE_TIME, MT4_TRADES.TICKET, MT4_TRADES.SYMBOL, MT4_TRADES.OPEN_PRICE, MT4_TRADES.CLOSE_PRICE, MT4_TRADES.COMMISSION, MT4_TRADES.SWAPS, MT4_TRADES.CMD from (MT4_TRADES join MT4_USERS ON MT4_TRADES.LOGIN=MT4_USERS.LOGIN) join MT4_GROUPS ON MT4_USERS.GROUP=MT4_GROUPS.GROUP where MT4_TRADES.LOGIN like '%{account_no}%' and MT4_TRADES.CMD = '1' and MT4_GROUPS.COMPANY like '%Henan Xinluan Information%' ")

        _1_cmd_data = cursor.fetchall()
        for cmd_1 in _1_cmd_data:
            if cmd_1[5].startswith('X'):
                fi_val = (cmd_1[7]-cmd_1[6])*100
            else:
                fi_val = (cmd_1[7]-cmd_1[6])*100000
            sell_point_list.append(fi_val)

            if str(cmd_1[1]).startswith('-'):
                pass
            else:
                profttradesinsell.append(cmd_1[1])

        if sell_point_list:
            sell_max = max(sell_point_list)
            sell_min = min(sell_point_list)
        else:
            pass

        cursor.execute(f"select MT4_TRADES.VOLUME, MT4_TRADES.PROFIT, MT4_TRADES.OPEN_TIME, MT4_TRADES.CLOSE_TIME, MT4_TRADES.TICKET, MT4_TRADES.SYMBOL, MT4_TRADES.OPEN_PRICE, MT4_TRADES.CLOSE_PRICE, MT4_TRADES.COMMISSION, MT4_TRADES.SWAPS, MT4_TRADES.CMD from (MT4_TRADES join MT4_USERS on MT4_TRADES.LOGIN=MT4_USERS.LOGIN) join MT4_GROUPS on MT4_USERS.GROUP=MT4_GROUPS.GROUP where MT4_TRADES.LOGIN like '%{account_no}%' and MT4_TRADES.CMD = '0' and MT4_GROUPS.COMPANY like '%Henan Xinluan Information%' ")

        _0_cmd_data = cursor.fetchall()
        for cmd_0 in _0_cmd_data:
            if cmd_0[5].startswith('X'):
                final_val = (cmd_0[7]-cmd_0[6])*100
            else:
                final_val = (cmd_0[7]-cmd_0[6])*100000
            buy_points_list.append(final_val)

            if str(cmd_0[1]).startswith('-'):
                    pass
            else:
                profttradesinbuy.append(cmd_0[1])

        if buy_points_list:
            buy_max = max(buy_points_list)
            buy_min = min(buy_points_list)
        else:
            pass

        cursor.execute(f"select MT4_TRADES.PROFIT from (MT4_TRADES JOIN MT4_USERS ON MT4_TRADES.LOGIN=MT4_USERS.LOGIN) JOIN MT4_GROUPS ON MT4_USERS.GROUP=MT4_GROUPS.GROUP where MT4_TRADES.LOGIN like '%{account_no}%' and MT4_TRADES.SYMBOL = '' and MT4_GROUPS.COMPANY like '%Henan Xinluan Information%' ")

        withdarw = cursor.fetchall()
        for withdr in withdarw:
            withdra_list = list(withdr)
            withd_amt = withdra_list[0]
            if str(withd_amt).startswith('-'):
                number = str(withd_amt).replace("-", "")
                withdraw_list.append(float(number))
            else:
                deposit_list.append(withd_amt)

        cursor.execute(f"select MT4_TRADES.PROFIT from (MT4_TRADES JOIN MT4_USERS ON MT4_TRADES.LOGIN=MT4_USERS.LOGIN) JOIN MT4_GROUPS ON MT4_USERS.GROUP=MT4_GROUPS.GROUP where MT4_TRADES.LOGIN like '%{account_no}%' and MT4_TRADES.COMMENT = '' and MT4_GROUPS.COMPANY like '%Henan Xinluan Information%' ")

        proft_best_worst = cursor.fetchall()
        for profit in proft_best_worst:
            profit_list = list(profit)
            best_worst_trade.append(profit_list[0])

        if best_worst_trade:
            worst_trade_value = min(best_worst_trade)
            best_trade_value = max(best_worst_trade)
        else:
            pass
        

    total_points = sum(buy_points_list)+sum(sell_point_list)

    if sell_max > buy_max:
        best_trade = sell_max
    else:
        best_trade = buy_max

    if sell_min > buy_min:
        worst_trade = buy_min
    else:
        worst_trade = sell_min

    context['key_data'] = key_data
    context['values_graph_data'] = values_graph_data
    # context['graph_values'] = list_graph_val
    context['closed_positions'] = all_list
    context['open_positions'] = open_posit_list
    context['best_trade_value'] = best_trade_value
    context['worst_trade_value'] = worst_trade_value

    if _0_cmd_data:
        context['profitable_long_trades'] = len(profttradesinbuy)/len(_0_cmd_data)*100
    else:
        pass

    if _1_cmd_data:
        context['profitable_short_trades'] = len(profttradesinsell)/len(_1_cmd_data)*100
    else:
        pass

    context['avg_win'] = avg_win
    context['avg_loss'] = avg_loss

    if data_sql:
        context['profitability'] = (len(profit_trades_list)/len(data_sql))*100
    else:
        pass

    context['total_points'] = total_points
    context['profit_factor'] = profit_factor
    context['total_volume'] = sum(vol_list)
    context['close_p_l'] = sum(profit_list)
    context['total_trades'] = len(data_sql)

    # if vol_list:
    #     context['highest_trade'] = max(vol_list)
    #     context['lowest_trade'] = min(vol_list)
    # else:
    #     pass

    context['avg_order_duration'] = duration

    context['total_deposit'] = sum(deposit_list)
    context['wallet_withdrawls'] = sum(withdraw_list)
    context['best_trade_points'] = best_trade
    context['worst_trade_points'] = worst_trade

    oview_data = f'https://crm.divsolution.com/api/v1/live_accounts/{request.user.id}/'
    get_overview_data = requests.get(oview_data).json()
    for data in get_overview_data['data']:
        try:
            if data['login'] == account_no:
                context['acc_no'] = data['login']
                context['balance'] = data['balance']
                context['equity'] = data['equity']
                context['margin'] = data['margin']
                context['free_margin'] = data['margin_free']
                context['margin_level'] = data['margin_level']
                date_split = data['added_on'].split('T')[0]
                context['added_on'] = date_split
        except:
            pass

    wallet = WalletFinance.objects.filter(list_display=True, user_id=request.user.id).order_by('-id')
    transaction = Transaction_Method.objects.filter(user_id=request.user.id).order_by('-id')

    for i in transaction:
        date_split = str(i.added_on).split(' ')[0]
        year_val = date_split.split('-')[0]
        month_val = date_split.split('-')[1]
        date_val = date_split.split('-')[2]
        id = i.id
        t = i.type
        amount = i.amount
        currency = i.currency
        comments = i.comments.name
        if comments == "Virtual currency":
            currency_type = "Crypto"
        else:
            currency_type = "USDT"
        if t == '1':
            transfer_type = "Deposit"
        else:
            transfer_type = "Withdrawal"
        response_list.append((year_val+month_val+date_val, {
            'added_on_year_val': year_val,
            'added_on_month_val': month_val,
            'added_on_date_val': date_val,
            'id':id,
            'added_on':i.added_on,
            'transfer_type':transfer_type,
            'currency':"usd",
            'comments':comments,
            'amount':amount,
            'get_status_display':"Completed"
        }))

    for i in wallet:

        date_split = str(i.added_on).split(' ')[0]
        year_val = date_split.split('-')[0]
        month_val = date_split.split('-')[1]
        date_val = date_split.split('-')[2]

        if i.type == 1:
            transfer_type = 'Deposit'
            type = 'Transfer IN'
        elif i.type == 2:
            transfer_type = 'Withdrawal'
            type = 'Transfer OUT'

        if i.details.startswith('Transfer from'):
            transfer_to = i.details.replace('Transfer from','')
        elif i.details.startswith('Transfer to'):
            transfer_to = i.details.replace('Transfer to','')
        elif i.details.startswith('Transfer Out'):
            transfer_to = i.details.replace('Transfer Out','')
        elif i.details.startswith('Transfer IN'):
            transfer_to = i.details.replace('Transfer IN','')
        if i.status == 0:
            get_status_display = 'Completed'
        elif  i.status == 1:
            get_status_display = 'Not Processed'
        if i.currency == 'USD':
            currency = 'usd'

        response_list.append((year_val+month_val+date_val, {
            'wallet':wallet,
            'amount':round(i.amount, 2),
            'type':type,
            'added_on':i.added_on,
            'currency':currency.upper(),
            'get_status_display':get_status_display,
            'added_on_year_val': year_val,
            'added_on_month_val': month_val,
            'added_on_date_val': date_val,
            'transfer_to':transfer_to,
            'transfer_type':transfer_type
        }))

    response_data = [d[1] for d in sorted(response_list, key=lambda x:x[0])]
    context['response_list'] = response_data

    return render(request,'clientportal/accountoverview.html', context=context)


def open_position(request):
    return render(request, 'clientportal/open_position.html', context=context)


def support(request):
    return render(request,'clientportal/support.html')


@login_required(login_url='login_client')
def downplat(request):
    return render(request,'clientportal/downplat.html')

def deposit(request):
    return render(request,'clientportal/deposit.html')


from django.contrib import messages

@login_required(login_url='login_client')
def addemail(request):

    # to_email = ''
    # admin_user = User.objects.all().filter(is_superuser=True)[0]
    r_email  = Register.objects.get(user_id=request.user.id).email
    if request.method == 'POST':
        r  = Register.objects.filter(user_id=request.user.id)
        previous_sec_email = r[0].secondaryemail
        secondary_email = request.POST['email']
        reason = request.POST['reason']
        if not r[0].email == secondary_email and not r[0].secondaryemail == secondary_email:
            r.update(secondaryemail=secondary_email, reasonsecondaryemail=reason)
            subject = "The User Added/Updated secondary Email"

            body = "The Updated Details are: \n\n"\
                "Client ID: \t{}".format(r[0].client_id)+'\n'+\
                "User: \t\t{}".format(r[0].uname.upper())+'\n'+\
                "Primary Email: {}".format(r[0].email)+'\n'+\
                "Previous secondary email: {}".format(previous_sec_email)+'\n'+\
                "Updated secondary email: {}".format(secondary_email)

            from_email = 'ditstaskmanager@gmail.com'
            # if admin_user.email:
            #     to_email = admin_user.email
            # else:
            #     to_email = from_email

            send_mail(
                subject,
                body,
                from_email,
                [from_email, r_email],
                fail_silently=False,
            )

            return redirect('profile')
        else:
            messages.error(request, 'e-mail already taken..!')

    return render(request,'clientportal/addemail.html')


@login_required(login_url='login_client')
def addaddress(request):

    # to_email = ''
    # admin_user = User.objects.all().filter(is_superuser=True)[0]
    r_email = Register.objects.get(user_id=request.user.id).email
    if request.method == 'POST':
        r  = Register.objects.filter(user_id=request.user.id)
        previous_address = r[0].address
        address = request.POST['address']
        r.update(address=address)
        # updated_address = r[0].address

        subject = "The User Address Update"

        body = "The Updated Details are: \n\n"\
            "Client ID: \t{}".format(r[0].client_id)+'\n'+\
            "User: \t\t{}".format(r[0].uname.upper())+'\n'+\
            "Previous Address: {}".format(previous_address)+'\n'+\
            "Updated Address: {}".format(address)

        from_email = 'ditstaskmanager@gmail.com'
        # to_email = from_email

        send_mail(
            subject,
            body,
            from_email,
            [from_email, r_email],
            fail_silently=False,
        )
        
        return redirect('profile')
    return render(request,'clientportal/profile.html')


def deposit_divepay(request):
    return render(request,'clientportal/depositdivepay.html')


def deposit_neteller(request):
    ca =  Addcurrency.objects.all()
    return render(request,'clientportal/depositneteller.html',{'ca':ca})


def deposit_skrill(request):
    ca =  Addcurrency.objects.all()
    return render(request,'clientportal/depositskrill.html',{'ca':ca})

@login_required(login_url='login_client')
def manage_funds(request):
    return render(request,'clientportal/managefunds.html')


def depositfailure(request):
    return render(request, 'clientportal/depositfailure.html')

@login_required(login_url='login_client')
def bitcoin_payment(request):
    return render(request, 'clientportal/bitcoinpayment.html')

@login_required(login_url='login_client')
def bitcoin_withdraw(request):
    return render(request, 'clientportal/bitcoin_withdraw.html')


@login_required(login_url='login_client')
def usdt(request):
    return render(request, 'clientportal/bitcoinpayment.html')

@login_required(login_url='login_client')
def usdt_withdraw(request):
    return render(request, 'clientportal/usdt_withdraw.html')


def depositsuccess(request):
    return render(request, 'clientportal/usdt.html')


def withdraw(request):
    return render(request,'clientportal/withdraw.html')

def live_account_response(request):
    return render(request,'clientportal/live_account_response.html')


def demo_account_response(request):
    return render(request,'clientportal/demo_account_response.html')


def withdraw_divepay(request):
    return render(request,'clientportal/withdraw_divepay.html')


def deposit_by_merchant(request):
    return render(request,'clientportal/deposit_by_merchant.html')

def withdraw_by_merchant(request):
    return render(request,'clientportal/withdraw_by_merchant.html')    

def testing_mail(request):
    send_to = "mbajaj2277@gmail.com"
    username = "mv3n0m"
    account_no = "111111"
    your_password = "123456789a"
    investor_pass = "1232431424"
    server_type = "Real"
    send_mail_func(send_to, username, account_no, your_password, investor_pass, server_type)
    return HttpResponse(send_to)


def send_mail_func(send_to=None, username=None, account_no=None, your_password=None, investor_pass=None, server_type=None,*args, **kwargs):
    data = {
        'user': username.title(),
        'login_account': account_no,
        'pwd': your_password,
        # 'inpwd': investor_pass,
        'server': server_type,
    }
    msg_text = """亲  {user},
    
恭喜您，您刚刚开设了一个新的真实账户！
您的账户信息如下，请您妥善保管您的信息，以免造成损失：

帐号：{login_account}
密码：{pwd}
服务器：{server}

顺祝您交易顺利！ 
""".format(**data)
    from_mail = 'ditstaskmanager@gmail.com'
    if send_to and your_password and account_no:
        send_mail("Your Account Details", msg_text, from_mail, [send_to], fail_silently=False)


def send_mail_func_demo(send_to=None, username=None, account_no=None, your_password=None, investor_pass=None, server_type=None,*args, **kwargs):
    data = {
        'user': username.title(),
        'login_account': account_no,
        'pwd': your_password,
        'server': server_type,
    }
    msg_text = """亲 {user},

恭喜您，您刚刚开设了一个新的模拟账户！您的账户信息，请妥善保管您的信息，以免造成损失 ：

帐号 ： {login_account}
密码 ： {pwd}
服务器 :  {server}


预祝您交易愉快和成功。

顺祝商祺
""".format(**data)

    from_mail = 'ditstaskmanager@gmail.com'
    if send_to and your_password and account_no:
        send_mail("Your Account Details", msg_text, from_mail, [send_to], fail_silently=False)


from clientportal.models import LiveAcAmount, DemoAcAmount

def live_account_open_api_call(request_data):

    jwt_dict_data = {}
    url = 'https://demodc.use.6i.nullpoint.io/accountopen'

    if request_data.POST.get('acctype') == 'Standard':
        jwt_dict_data = jwt_decode.dict_data
    elif request_data.POST.get('acctype') == 'Premium':
        jwt_dict_data = jwt_decode.dict_data
    elif request_data.POST.get('acctype') == 'VIP':
        jwt_dict_data = jwt_decode.dict_data
    else:
        jwt_dict_data = jwt_decode.dict_data

    jwt_dict_data['server'] = "Real"
    # jwt_dict_data['leverage'] = "1000"
    jwt_dict_data['currency'] = request_data.POST.get('ctype')
    jwt_dict_data['country'] = request_data.user.register.country
    jwt_dict_data['password'] = make_password()
    jwt_dict_data['investor_pass'] = make_password()
    jwt_dict_data['client_name'] = request_data.user.register.uname
    jwt_dict_data['client_email'] = request_data.user.register.email
    # camp = request_data.user.register.registerusercampaign_set
    # if camp.exists():
    #     jwt_dict_data['comment'] = "{0},{1}".format(
    #          request_data.user.register.registerusercampaign_set.first().campaign_code,
    #          request_data.user.register.registerusercampaign_set.first().ref_code
    #     )
    x_forwarded_for = request_data.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(',')[0]
    else:
        client_ip = request_data.META.get('REMOTE_ADDR')
    jwt_dict_data['client_ip'] = client_ip
    encoded_return_data = "request_message={0}".format(encode_jwt(data=jwt_dict_data))
    response_api = requests.post(url, data=encoded_return_data, verify=False)
    return {"data": decode_jwt(data=response_api.text), "server": jwt_dict_data['server']}


from clientportal.models import LiveAcAmount, DemoAcAmount
from sportapp.models import RegisterUserCampaign
from sportapp.models import Mt4users

@login_required(login_url='login_client')
def laccount(request):

    # acs = []
    # response_data = {}
    # try:
    #     if Register.objects.get(user=request.user.id).acc_type.all().exists():
    #         acs=Register.objects.get(user=request.user.id).acc_type.all()
    #     else:
    #         acs=Addaccounttype.objects.all()
    # except:
    #     pass

    ref_id = 0
    ref_camp_code = ''
    ref_camp_name = ''
    register_id = request.user.register
    
    try:
        reg_ref_code = RegisterUserCampaign.objects.filter(register=register_id).first()
        ref_id = reg_ref_code.ref_code
        ref_camp_code = reg_ref_code.campaign_code
        ref_camp_name = reg_ref_code.campaign
    except Exception as e:
        print('----exception in uper---', e)
        pass

    if request.method == "POST":
        ac = request.POST.get('acctype')
        ct = request.POST.get('ctype')
        # if len(LiveAccount.objects.filter(user_id=request.user.id)) < 4:
        # if len(LiveAccount.objects.filter(user_id=request.user.id))+1 < int(Register.objects.get(user=request.user.id).acc_limit):

        response_data = live_account_open_api_call(request)
        r_data = response_data['data']
        mt4_login = r_data.get('login')

        laccount_obj = LiveAccount(ac_type=ac, cu_type=ct, user_id=request.user.id, account_no=r_data.get('login'), balance=r_data.get('balance'), equity=r_data.get('equity'), group=r_data.get('group'))
        laccount_obj.save()

        lamount = LiveAcAmount(user=request.user, liveaccount=laccount_obj, amount=r_data['leverage'])
        lamount.save()

        # try:
        try:
            reg_camp_insta = RegisterUserCampaign.objects.get(register=register_id, mt4_id=0, status=1)

            if reg_camp_insta:
                reg_camp_insta.mt4_id = mt4_login
                reg_camp_insta.save()
            else:
                # reg_obj = RegisterUserCampaign.objects.create(register=register_id, mt4_id=mt4_login, ref_code=ref_id, campaign_code=ref_camp_code, campaign=ref_camp_name, status=1)
                reg_obj = RegisterUserCampaign.objects.create(register=register_id, mt4_id=mt4_login, ref_code=0, campaign_code='', campaign='', status=1)
                reg_obj.save()
        except Exception as e:
            print('----exception in live account create-----', e)
            # reg_objs = RegisterUserCampaign.objects.create(register=register_id, mt4_id=mt4_login, ref_code=ref_id, campaign_code=ref_camp_code, campaign=ref_camp_name, status=1)
            reg_objs = RegisterUserCampaign.objects.create(register=register_id, mt4_id=mt4_login, ref_code=0, campaign_code='', campaign='', status=1)
            reg_objs.save()
        # except Exception as e:
        #     reg_objs = RegisterUserCampaign.objects.create(register=register_id, mt4_id=mt4_login, status=1)
        #     reg_objs.save()

        print("New Live mt4 Created---|account number|-", r_data.get('login'), '|Password|-', r_data.get('password'), '|Investor Password|-', r_data.get('investor_pass'))

        send_mail_func(
            send_to=r_data.get('email'),
            username=r_data.get('name'),
            account_no=r_data.get('login'),
            your_password=r_data.get('password'),
            # investor_pass=r_data.get('investor_pass'),
            server_type=response_data['server'],
        )

        return redirect(live_account_response)
        # else:
        #     messages.info(request, 'You have reached your limit, please contact Admin for further account access..!')
    # else:
    #     context_data = {'ac':ac, 'ca':Addcurrency.objects.all()}
    return render(request,'clientportal/laccount.html', {'ac':Addaccounttype.objects.all(), 'ca':Addcurrency.objects.all()})


@login_required(login_url='login_client')
def demo_account_open_api_call(request_data):
    url = 'https://demodc.use.6i.nullpoint.io/accountopen'
    jwt_dict_data = jwt_decode.dict_data_demo
    jwt_dict_data['server'] = "Demo"
    jwt_dict_data['currency'] = request_data.POST.get('ctype')
    jwt_dict_data['country'] = request_data.user.register.country
    jwt_dict_data['password'] = make_password()
    jwt_dict_data['investor_pass'] = make_password()
    jwt_dict_data['client_name'] = request_data.user.username
    jwt_dict_data['client_email'] = request_data.user.register.email
    jwt_dict_data['client_ip'] = request_data.META['REMOTE_ADDR']
    x_forwarded_for = request_data.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        client_ip = x_forwarded_for.split(',')[0]
    else:
        client_ip = request_data.META.get('REMOTE_ADDR')
    jwt_dict_data['client_ip'] = client_ip
    encoded_return_data = "request_message={0}".format(encode_jwt(data=jwt_dict_data))
    response_api = requests.post(url, data=encoded_return_data, verify=False)
    return {"data": decode_jwt(data=response_api.text), "server": jwt_dict_data['server']}


def daccount(request):

    # ac = Register.objects.get(user=request.user.id)
    response_data = {}

    if request.method == "POST":
        ac = request.POST['accounttype']
        ct = request.POST['ctype']
        # if len(DemoAccount.objects.filter(user_id=request.user.id))+1 < int(Register.objects.get(user=request.user.id).demo_acc_limit):
        response_data = demo_account_open_api_call(request)
        r_data = response_data['data']
        daccount_obj = DemoAccount(ac_type=ac, cu_type=ct, user_id=request.user.id, account_no=r_data.get('login'),
                                    balance=r_data.get('balance'), equity=r_data.get('equity'), group=r_data.get('group'))
        daccount_obj.save()
        damount = DemoAcAmount(user=request.user, demoaccount=daccount_obj, amount=r_data['leverage'])
        damount.save()
        print("New Demo mt4 Created---|acount number|-",r_data.get('login'), '|Password|-', r_data.get('password'), '|Investor Password|-', r_data.get('investor_pass'))
        send_mail_func_demo(
            send_to=r_data.get('email'),
            username=r_data.get('name'),
            account_no=r_data.get('login'),
            your_password=r_data.get('password'),
            investor_pass=r_data.get('investor_pass'),
            server_type=response_data['server'],
        )
        return redirect(demo_account_response)
        # else:
        #     messages.info(request, 'You have reached your limit, please contact Admin for further account access..!')
    # else:
    #     context_data ={'ac':Addaccounttype.objects.all(), 'ca':Addcurrency.objects.all()}
    return render(request,'clientportal/daccount.html', {'ac':Addaccounttype.objects.all(), 'ca':Addcurrency.objects.all()})


class GetLiveAccountDetailsView(View):
    def account_detail_url(self, request_data):
        url = "https://demodc.use.6i.nullpoint.io/accountget"
        jwt_dict_data = jwt_decode.live_account_data
        account_no = request_data.user.liveaccount_set.first().account_no
        jwt_dict_data['account'] = "{}".format(account_no) if account_no else None
        if not jwt_dict_data['account']:
            return {'status': 0, 'msg': HttpResponse('Your instance not exist in LiveAccount instance.')}
        encoded_return_data = "request_message={0}".format(encode_jwt(data=jwt_dict_data))
        response_api = requests.post(url, data=encoded_return_data, verify=False)
        return decode_jwt(data=response_api.text)

    def get(self, request, *args, **kwargs):
        data = self.account_detail_url(self.request)
        if data['status'] == 0:
            return data['msg']
        return HttpResponse("Live account detail")


class GetDemoAccountDetailsView(View):
    def account_detail_url(self, request_data):
        url = "https://demodc.use.6i.nullpoint.io/accountget"
        jwt_dict_data = jwt_decode.demo_account_data
        account_no = request_data.user.demoaccount_set.first().account_no
        jwt_dict_data['account'] = "{}".format(account_no) if account_no else None
        if not jwt_dict_data['account']:
            return {'status': 0, 'msg': HttpResponse('Your instance not exist in LiveAccount instance.')}
        encoded_return_data = "request_message={0}".format(encode_jwt(data=jwt_dict_data))
        response_api = requests.post(url, data=encoded_return_data, verify=False)
        return decode_jwt(
            data=response_api.text)

    def get(self, request, *args, **kwargs):
        data = self.account_detail_url(self.request)
        if data['status'] == 0:
            return data['msg']
        return HttpResponse("Demo account detail")

def settings(request):
    return render(request,'clientportal/settings.html')

def performance(request):
    return render(request,'clientportal/performance.html')


# cursor.execute(f"select MT4_TRADES.PROFIT from(MT4_TRADES join MT4_USERS on MT4_TRADES.LOGIN=MT4_USERS.LOGIN) join MT4_GROUPS on MT4_USERS.GROUP=MT4_GROUPS.GROUP where MT4_TRADES.LOGIN like '%{log}%' and MT4_TRADES.COMMENT = '' and MT4_TRADES.CLOSE_TIME = '1970-01-01 00:00:00' and MT4_GROUPS.COMPANY like '%Henan Xinluan Information%' ")