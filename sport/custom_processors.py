from common.choices import (
    CustomDateFilter
)
import requests
from clientportal .models import Uploaddocument,UserWallet
from sportapp.models import Register
from django.shortcuts import get_object_or_404


def custom_date_filter(request):

    user=None
    document = None
    wallet=None
    dob_year = None
    dob_month = None
    dob_date = None
    year_val = None
    month_val = None
    date_val = None

    try:
        user_id = request.GET.get('u_id')
    except:
        pass

    if user_id:
        user = Register.objects.get(user=user_id)
        document = Uploaddocument.objects.filter(user=user_id)
        wallet = UserWallet.objects.get(user=user_id)

    if user:
        date_split = str(user.added_on).split(' ')[0]
        year_val = date_split.split('-')[0]
        month_val = date_split.split('-')[1]
        date_val = date_split.split('-')[2]
        dob_datesplit = str(user.dob).split('-')
        dob_year = dob_datesplit[0]
        dob_month = dob_datesplit[1]
        dob_date = dob_datesplit[2]
        return {
        'custom_date_choice': CustomDateFilter.CHOICES,
        'user':user,
        'document':document,
        'wallet':wallet,
        'dob_year':dob_year,
        'dob_month':dob_month,
        'dob_date':dob_date,
        'added_on_year_val': year_val,
        'added_on_month_val': month_val,
        'added_on_date_val': date_val,
        }
    return {
        'custom_date_choice': CustomDateFilter.CHOICES,
        #'user':user,
        'document':document,
        'wallet':wallet,
        'dob_year':dob_year,
        'dob_month':dob_month,
        'dob_date':dob_date,
        'added_on_year_val': year_val,
        'added_on_month_val': month_val,
        'added_on_date_val': date_val,
        }


def ib_wallet(request):

    url = 'http://ib-portal.hnxinluan.cn/api/v1/ib_users'
    req = requests.get(url)
    req_json = req.json()
    ib_id = 0
    ib_user = ''

    for user in req_json:
        user_id = request.GET.get('u_id')
        if not user_id:
            return {}
        user_id = Register.objects.get(user__id=user_id)
        client_id = user_id.client_id
        if user['client_id'] == client_id:
            ib_user = 'exists'
            ib_id = user['ib_id']
            break

        # if client_id ==
    detail_api = f'http://ib-portal.hnxinluan.cn/api/v1/get_commission/{ib_id}'
    req = requests.get(detail_api)
    req_json = req.json()

    if req_json['commission']:
        wallet = req_json['commission'][0]['wallet']
        if not wallet:
            wallet = 0.00
    else:
        wallet = 0.00

    return {
        'ib_wallet': wallet,
        'ib_user':ib_user,
    }
