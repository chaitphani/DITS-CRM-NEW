from itertools import chain
from django.urls import reverse
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
import sys

from django.contrib.auth.models import User
from clientportal.jwt_decode import (
    encode_jwt, decode_jwt
)
from django.core.mail import EmailMultiAlternatives
from clientportal import jwt_decode
from clientportal.models import (
    LiveAccount, DemoAccount, UserDeposits, UserDepositApproval, UserWithdraw,
    WalletFinance
)
from django.conf import settings
from clientportal.models import (
    UserWallet, WalletFinance
)
import requests
import json
import random
import string
from clientportal.ip_tracker import IPTracker
from datetime import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def render_response(data=None, status=None, error=None):
    '''
    This function is for render data response for front-end
    '''
    # 0 => True
    # 1 => False
    response_data = {'data': [], 'status': None, 'error': []}
    if status == 1:
        response_data['status'] = 1
        response_data['error'] = error if error else "Not provided error message."
        return Response(response_data)
    response_data['data'] = data if data else []
    response_data['status'] = 0
    return Response(response_data)


def api_call_jwt(url=None, jwt_dict_data=None):
    if not jwt_dict_data and url:
        return "please provide url, jwt_dict_data"
    encoded_return_data = "request_message={0}".format(encode_jwt(data=jwt_dict_data))
    response_api = requests.post(url, data=encoded_return_data, verify=False)
    return decode_jwt(data=response_api.text)


class GetAccountDetailAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication,)

    url = "https://demodc.use.6i.nullpoint.io/accountget"

    # def account_detail_api(self, dict_data=None):
    #     if dict_data:
    #         encoded_return_data = "request_message={0}".format(encode_jwt(data=dict_data))
    #         response_api = requests.post(self.url, data=encoded_return_data, verify=False)
    #         ac = decode_jwt(data=response_api.text)
    #         # return decode_jwt(data=response_api.text)
    #         print('check ac deetail',ac)
    #         return ac

    def account_detail_api(self, dict_data=None):
        if dict_data:
            # print('dict_data--------------->', dict_data)
            encoded_return_data = "request_message={0}".format(encode_jwt(data=dict_data))
            #print('encoded_return_data---->', encoded_return_data)
            response_api = requests.post(self.url, data=encoded_return_data, verify=False)
            #print('respons_api---->', response_api)
            return decode_jwt(data=response_api.text)

    def get_account_number(self):
        list_var = chain(self.request.user.demoaccount_set.all(), self.request.user.liveaccount_set.all())
        print('check api ', list_var)
        return sorted(list_var, key=lambda instance: instance.added_on)

    def get_all_account_data(self):
        model_account_data = self.get_account_number()
        lst = []
        for i in enumerate(model_account_data, 1):
            print('Inside for loop-------------------')
            api_data = jwt_decode.account_get_data
            api_data['account'] = "{0}".format(i[1].account_no)
            print('check ac no', api_data['account'])
            api_data['server'] = "Demo" if i[1].type == 1 else "Real"
            print('check server', api_data['server'])
            api_data_var = self.account_detail_api(api_data)
            print('ac detail api', api_data_var)
            if i[1].type == 1:
                print("in if------------------%%%%%%%%%%%%%")
                api_data_var['server_title'] = "模拟账户"
            else:
                api_data_var['server_title'] = "真实"
            api_data_var['type'] = i[1].type
            api_data_var['server_type'] = i[1].type

            if i[1].cu_type == "USD":
                print("in if------------------%%%%%%%%%%%%%")
                api_data_var['cu_type'] = "美元"

            api_data_var['s_no'] = i[0]
            if i[1].ac_type == "Standard" or i[1].ac_type == "标准账户":
                print("in if------------------%%%%%%%%%%%%%")
                api_data_var['ac_type'] = "标准账户"
            elif i[1].ac_type == "Demo" or i[1].ac_type == "模拟账户":
                print("in if------------------%%%%%%%%%%%%%")
                api_data_var['ac_type'] = "模拟账户"

            elif i[1].ac_type == "undefined" or i[1].ac_type == "Standard Demo":
                print("in if------------------%%%%%%%%%%%%%")
                api_data_var['ac_type'] = "未定义"

            lst.append(api_data_var)
            print('all list', lst)
        return lst

    def get(self, *args, **kwargs):
        data_var = self.get_all_account_data()
        print('!!!!!!!!!!!!!!!!!!!!!!!!', data_var)
        return render_response(data=data_var, status=0)


class UserAccountOverViewAPIView(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)

    user_account_data = dict()

    user_account_get_api = 'https://demodc.use.6i.nullpoint.io/accountget'

    user_info_get_api = 'https://demodc.use.6i.nullpoint.io/userinfoget'

    def account_detail_api(self, url=None, dict_data=None):
        encoded_return_data = "request_message={0}".format(encode_jwt(data=dict_data))
        response_api = requests.post(url, data=encoded_return_data, verify=False)
        return decode_jwt(data=response_api.text)

    def get(self, *args, **kwargs):
        account_data, type = LiveAccount.objects.filter(account_no=int(self.kwargs.get('account'))), 0
        #self.user_account_data['created_date'] = account_data.first().added_on
        if not account_data.exists():
            account_data, type = DemoAccount.objects.filter(account_no=int(self.kwargs.get('account'))), 1
            # self.user_account_data['created_date'] = account_data.first().added_on
        jwt_dict_data = jwt_decode.account_get_data
        jwt_dict_data['account'] = "{0}".format(account_data.first().account_no)
        jwt_dict_data['server'] = "Demo" if type == 1 else "Real"
        self.user_account_data['account_get_data'] = self.account_detail_api(self.user_account_get_api, jwt_dict_data)
        self.user_account_data['account_info_get_data'] = self.account_detail_api(self.user_info_get_api, jwt_dict_data)
        return render_response(data=self.user_account_data, status=0)


class UserLiveAccountAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication,)

    user_model = User

    live_account_api_url = "https://demodc.use.6i.nullpoint.io/userinfoget"

    def request_send(self, jwt_dict_data=None, url=None):
        encoded_return_data = "request_message={0}".format(encode_jwt(data=jwt_dict_data))
        response_api = requests.post(url, data=encoded_return_data, verify=False)
        return decode_jwt(data=response_api.text)

    def get(self, *args, **kwargs):
        if not self.kwargs.get('user_id'):
            return render_response(status=1, error="Please provide user_id params in get.")
        user_obj = self.user_model.objects.filter(id=self.kwargs.get('user_id'))
        if not user_obj.exists():
            return render_response(status=1, error="Please provide vaild user_id params in get.")
        lst = []
        for i in user_obj.first().liveaccount_set.all():
            api_data = jwt_decode.account_get_data
            api_data['account'] = "{0}".format(i.account_no)
            api_data['server'] = "Real"
            data = self.request_send(jwt_dict_data=api_data, url=self.live_account_api_url)
            data['cu_type'] = i.cu_type
            data['added_on'] = i.added_on
            lst.append(data)
        return render_response(data=lst, status=0)


class UserDemoAccountAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication,)

    user_model = User

    live_account_api_url = "https://demodc.use.6i.nullpoint.io/userinfoget"

    def request_send(self, jwt_dict_data=None, url=None):
        encoded_return_data = "request_message={0}".format(encode_jwt(data=jwt_dict_data))
        response_api = requests.post(url, data=encoded_return_data, verify=False)
        return decode_jwt(data=response_api.text)

    def get(self, *args, **kwargs):
        if not self.kwargs.get('user_id'):
            return render_response(status=1, error="Please provide user_id params in get.")
        user_obj = self.user_model.objects.filter(id=self.kwargs.get('user_id'))
        if not user_obj.exists():
            return render_response(status=1, error="Please provide vaild user_id params in get.")
        lst = []
        for i in user_obj.first().demoaccount_set.all():
            api_data = jwt_decode.account_get_data
            api_data['account'] = "{0}".format(i.account_no)
            api_data['server'] = "Demo"
            data = self.request_send(jwt_dict_data=api_data, url=self.live_account_api_url)
            data['cu_type'] = i.cu_type
            data['added_on'] = i.added_on
            lst.append(data)
        return render_response(data=lst, status=0)


class AccountEditAPIView(APIView):

    def account_edit_api(self, request_data):
        url = "https://demodc.use.6i.nullpoint.io/accountedit"
        jwt_dict_data = jwt_decode.edit_account
        account_no = request_data.user.liveaccount_set.first().account_no
        jwt_dict_data['account'] = "{}".format(account_no) if account_no else None
        if not jwt_dict_data['account']:
            return {'status': 0, 'msg': HttpResponse('Your instance not exist in LiveAccount instance.')}
        #
        # Please mention all the things from post data for edit.
        #
        return api_call_jwt(url, jwt_dict_data)

    def post(self, request, *args, **kwargs):
        data = self.account_edit_api(self.request)
        if data['status'] == 0:
            return data['msg']
        # save your data.
        return HttpResponse('Account edit')


class AccountPwdResetView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def send_mail(self, user_email=None, account=None, password=None):
        data = {
            'account': account,
            'password': password
        }
        msg = '''Your New password
Account: {account}
Password: {password}
        '''.format(**data)
        email = EmailMultiAlternatives("Password Change", msg, settings.EMAIL_HOST_USER, [user_email])
        email.attach_alternative(msg, 'text/pain')
        email.send()

    def make_password(self, stringLength=15):
        password_characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(password_characters) for i in range(stringLength))

    def get_user_email(self, type=None, account=None):
        if type == 0:
            a = LiveAccount.objects.filter(account_no=int(account))
            if a.exists():
                return a.first().user.email
        elif type == 1:
            a = DemoAccount.objects.filter(account_no=int(account))
            if a.exists():
                return a.first().user.email

    def account_reset_pwd(self, account=None, type=None):
        url = 'https://demodc.use.6i.nullpoint.io/resetpwd'
        jwt_dict_data = jwt_decode.reset_account_pwd
        jwt_dict_data['account'] = "{0}".format(account)
        jwt_dict_data['server'] = "Real" if int(type) == 0 else "Demo"
        jwt_dict_data['password'] = self.make_password()
        if not jwt_dict_data['account']:
            return {'status': 0, 'msg': HttpResponse('Your instance not exist in LiveAccount instance.')}
        # your password data
        a = api_call_jwt(url, jwt_dict_data)
        if a.get('response') == "SUCCESS":
            self.send_mail(
                account=jwt_dict_data.get('account'),
                password=jwt_dict_data.get('password'),
                user_email=self.get_user_email(
                    type=int(type),
                    account=int(jwt_dict_data['account'])
                )
            )

    def get(self, *args, **kwargs):
        user_account = self.request.GET.get('account') if self.request.GET.get('account') else False
        server_type = self.request.GET.get('type') if self.request.GET.get('type') else False
        if user_account and server_type:
            a = self.account_reset_pwd(
                account=int(user_account),
                type=int(server_type)
            )
        return redirect(
            reverse('settings') + "?account={0}".format(
                user_account if user_account else ""
            )
        )

    def post(self, request, *args, **kwargs):
        data = self.account_reset_pwd(self.request)
        if data['status'] == 0:
            return data['msg']
        # save your data
        return HttpResponse('Account reset API')


class InvestorPasswordView(APIView):

    def account_investor_pwd(self, request_data):
        url = 'https://demodc.use.6i.nullpoint.io/resetinvpwd'
        jwt_dict_data = jwt_decode.investor_password_pwd
        account_no = request_data.user.liveaccount_set.first().account_no
        jwt_dict_data['account'] = "{}".format(account_no) if account_no else None
        if not jwt_dict_data['account']:
            return {'status': 0, 'msg': HttpResponse('Your instance not exist in LiveAccount instance.')}
        # investor pwd post
        return api_call_jwt(url, jwt_dict_data)

    def post(self, request, *args, **kwargs):
        data = self.account_investor_pwd(self.request)
        if data['status'] == 0:
            return data['msg']
        # save your data
        return HttpResponse('Account Investor API')


class CheckPWDView(APIView):

    def check_password(View):
        url = 'https://demodc.use.6i.nullpoint.io/checkpwd'
        jwt_dict_data = jwt_decode.check_password_dict
        account_no = request_data.user.liveaccount_set.first().account_no
        jwt_dict_data['account'] = "{}".format(account_no) if account_no else None
        if not jwt_dict_data['account']:
            return {'status': 0, 'msg': HttpResponse('Your instance not exist in LiveAccount instance.')}
        # post data
        return api_call_jwt(url, jwt_dict_data)

    def post(self, request, *args, **kwargs):
        data = self.check_password(self.request)
        if data['status'] == 0:
            return data['msg']
        print(data)
        return HttpResponse('CheckPWD')


class UserDepositCheckAPIView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    def post(self, *args, **kwargs):
        divepay_data_var = self.request.data.get('divepay_data')
        if not divepay_data_var:
            return render_response(status=1, error="require params.")
        self.request.session['divepay_data'] = json.loads(divepay_data_var)
        return render_response(status=0)


class StoreDetailsAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication,)

    walletfinance_model = WalletFinance
    userdeposit_model = UserDeposits

    def data_save_(self):
        a = IPTracker()
        return a.check_ip(self.request)

    def post(self, *args, **kwargs):
        data = self.data_save_()
        c = self.walletfinance_model.objects.create(
            user_id=self.request.user.id,
            client_id=self.request.user.register.client_id,
            name=self.request.user.username,
            country=self.request.user.register.country,
            t_ip=data.get('ip'),
            t_country=data.get('country_name'),
            details="Deposit from Divepay",
            amount=int(self.request.data.get('price')),
            currency="USD",
            status=1,
            list_display=False
        )
        c.save()
        self.userdeposit_model.objects.create(
            walletfinance_id=c.id,
            comment="",
            item_id=self.request.data.get('item_id'),
            action_choice=3,
        )
        return Response(data={'status': 0})


class CheckUserPaymentDivePayAPIView(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (SessionAuthentication,)

    user_wallet_model = UserWallet
    user_deposit_model = UserDeposits
    walletfinance_model = WalletFinance
    user_deposit_approval_model = UserDepositApproval

    def data_save_(self):
        a = IPTracker()
        return a.check_ip(self.request)

    def amount_added_on_wallet(self, payment_status=None, amount_divepay=None, user_id=None):
        if payment_status == 0:
            filter_u_wal = self.user_wallet_model.objects.get(
                user_id=user_id)
            filter_u_wal.amount += float(amount_divepay)
            filter_u_wal.save()
            return {'status': True}
        return {'status': False}

    def permission_deposit(self, item_id, payment_status, amount, dive_pay_post_data):
        user_deposit_model_obj = self.user_deposit_model.objects.get(item_id=item_id)
        user_deposit_approval_var = self.user_deposit_approval_model.objects.filter(user_id=user_deposit_model_obj.walletfinance.user_id)
        if user_deposit_approval_var.exists() and user_deposit_approval_var.first().approve:
            self.amount_added_on_wallet(
                payment_status=0 if payment_status == 0 else 1,
                amount_divepay=float(amount),
                user_id=user_deposit_model_obj.walletfinance.user_id)
            user_deposit_model_obj.comment = dive_pay_post_data.get('additional_message')
            user_deposit_model_obj.batch = dive_pay_post_data.get('trans_id')
            user_deposit_model_obj.action_choice = 2
            user_deposit_model_obj.save()
            a = self.walletfinance_model.objects.filter(id=user_deposit_model_obj.walletfinance.id)
            a.update(
                feededucted=dive_pay_post_data.get('fees'),
                status=0,
                list_display=True
            )
        else:
            user_deposit_model_obj.comment = dive_pay_post_data.get('additional_message')
            user_deposit_model_obj.batch = dive_pay_post_data.get('trans_id')
            user_deposit_model_obj.action_choice = 0
            user_deposit_model_obj.save()
            a = self.walletfinance_model.objects.filter(id=user_deposit_model_obj.walletfinance.id)
            a.update(
                feededucted=dive_pay_post_data.get('fees'),
                status=1,
                list_display=False
            )

    def post(self, *args, **kwargs):
        dive_pay_deposit_data = self.request.data
        if dive_pay_deposit_data['payment_status'] == "Completed":
            self.permission_deposit(dive_pay_deposit_data.get('item_id'),
                                    payment_status=0,
                                    amount=dive_pay_deposit_data.get('amount'),
                                    dive_pay_post_data=dive_pay_deposit_data)
            return redirect('DepositSuccessTemplateView')
        self.permission_deposit(dive_pay_deposit_data.get('item_id'), payment_status=1)
        return redirect('DepositFailureTemplateView')


class TransferAmountAPIView(APIView):
    permission_classes = ()
    authentication_classes = (SessionAuthentication,)
    '''
    payment_status: 0 => payment SUCCESS
    payment_status: 1 => payment not SUCCESS
    payment_status: 2 => not have balance
    '''
    payment_status = 0

    wallet_to_mt4_api_url = 'https://demodc.use.6i.nullpoint.io/deposit'
    mt4_to_wallet_api_url = 'https://demodc.use.6i.nullpoint.io/withdraw'

    user_wallet_model = UserWallet
    walletfinance_mdoel = WalletFinance

    def request_send(self, jwt_dict_data=None, url=None):
        encoded_return_data = "request_message={0}".format(encode_jwt(data=jwt_dict_data))
        response_api = requests.post(url, data=encoded_return_data, verify=False)
        return decode_jwt(data=response_api.text)

    def data_save_(self):
        try:

            a = IPTracker()
            return a.check_ip(self.request)
        except Exception as error:
            print("Error on line {}".format(sys.exc_info()[-1].tb_lineno), error)
            return str(error)

    def walletfinance_mdoel_create(self, type=None, transfer_from=None, transfer_from_to=None, amount=None, status=None):
        try:

            '''
            type: 1 -> Transfer IN.
            type: 2 -> Transfer OUT.
            '''
            if transfer_from == 'wal_0' and transfer_from_to != 'wal_0':
                data = self.data_save_(self)
                c = self.walletfinance_mdoel.objects.create(
                    user_id=self.request.user.id,
                    client_id=self.request.user.register.client_id,
                    name=self.request.user.username,
                    country=self.request.user.register.country,
                    t_ip=data.get('ip'),
                    t_country=data.get('country_name'),
                    type=type,
                    details="Transfer to MT4: {0}".format(transfer_from_to),
                    amount=float(amount),
                    currency="USD",
                    feededucted=0,
                    status=status
                )
                c.save()
            elif transfer_from != 'wal_0' and transfer_from_to == 'wal_0':
                data = self.data_save_()
                c = self.walletfinance_mdoel.objects.create(
                    user_id=self.request.user.id,
                    client_id=self.request.user.register.client_id,
                    name=self.request.user.username,
                    country=self.request.user.register.country,
                    t_ip=data.get('ip'),
                    t_country=data.get('country_name'),
                    type=type,
                    details="Transfer from MT4: {0}".format(transfer_from),
                    amount=float(amount),
                    currency="USD",
                    feededucted=0,
                    status=status
                )
                c.save()
        except Exception as error:
            print("Error on line {}".format(sys.exc_info()[-1].tb_lineno), error)
            return str(error)

    def wallet_to_mt4(self, transfer_from=None, transfer_from_to=None, amount=None):
        try:

            wall_amount1 = self.request.user.userwallet_set.first().amount - amount
            wall_amount = float(wall_amount1)
            print('waller_amount------', wall_amount)
            print("check all managefund activity --------------------$$$$$$$$$$$$$", transfer_from, transfer_from_to, amount, self.request.user.id)
            if wall_amount >= 0:
                jwt_dict_data = jwt_decode.deposit_data
                jwt_dict_data['amount'] = "{0}".format(str(amount))
                jwt_dict_data['account'] = "{0}".format(transfer_from_to)
                jwt_dict_data['comment'] = "Transfer Out A {0}, AC {1}".format(amount, transfer_from_to)

                data = self.request_send(jwt_dict_data, url=self.wallet_to_mt4_api_url)
                if data['response'] == "SUCCESS":
                    u_wall_filter = self.user_wallet_model.objects.filter(user_id=self.request.user.id)
                    u_wall_filter.update(amount=wall_amount)
                    self.payment_status = 0
                    self.walletfinance_mdoel_create(2, transfer_from, transfer_from_to, amount, self.payment_status)
                    return {'status': 0, 'data': self.payment_status, 'amount': u_wall_filter.amount}
                else:
                    self.payment_status = 1
                    self.walletfinance_mdoel_create(2, transfer_from, transfer_from_to, amount, self.payment_status)
                    return {'status': 0, 'data': self.payment_status, 'amount': amount}
            else:
                self.payment_status = 2
                return {'status': 0, 'data': self.payment_status, 'amount': amount}
        except Exception as error:
            print("Error on line {}".format(sys.exc_info()[-1].tb_lineno), error)
            return {'status': 0, 'data': 'data not found--------------------########'}

    def mt4_to_wallet(self, transfer_from=None, transfer_from_to=None, amount=None):
        jwt_dict_data = jwt_decode.withdraw_data
        jwt_dict_data['account'] = "{0}".format(str(transfer_from))
        jwt_dict_data['amount'] = "{0}".format(amount)
        jwt_dict_data['server'] = "Real"
        jwt_dict_data['comment'] = "Transfer IN A {0}, AC {1}".format(amount, transfer_from_to)
        data = self.request_send(jwt_dict_data, url=self.mt4_to_wallet_api_url)
        if data['response'] == "SUCCESS":
            u_wall_filter = self.user_wallet_model.objects.get(user_id=self.request.user.id)
            u_wall_filter.amount = u_wall_filter.amount + float(amount)
            u_wall_filter.save()
            self.payment_status = 0
            self.walletfinance_mdoel_create(1, transfer_from, transfer_from_to, amount, self.payment_status)
            return {'status': 0, 'data': self.payment_status, 'amount': u_wall_filter.amount}
        else:
            self.payment_status = 1
            self.walletfinance_mdoel_create(1, transfer_from, transfer_from_to, amount, self.payment_status)
            return {'status': 0, 'data': self.payment_status, 'amount': amount}

    def post(self, *args, **kwargs):
        transfer_from_var = self.request.data.get('transfer_from')
        transfer_from_to = self.request.data.get('transfer_from_to')
        print('transfer_from_var----->', transfer_from_var)
        print('transfer_from_to----->', transfer_from_to)
        amount_var = float(self.request.data.get('amount'))
        if transfer_from_var == 'wal_0' and transfer_from_to != 'wal_0':
            return_data = self.wallet_to_mt4(transfer_from_var, transfer_from_to, amount_var)
        elif transfer_from_var != 'wal_0' and transfer_from_to == 'wal_0':
            return_data = self.mt4_to_wallet(transfer_from_var, transfer_from_to, amount_var)
        else:
            return render_response(data={'payment_status': 3}, status=0)
        return render_response(data={'payment_status': return_data['data'], 'amount': return_data['amount']}, status=0)


class PaymentApproveDepositAPIView(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)

    model = UserDeposits
    user_wallet_model = UserWallet
    walletfinance_model = WalletFinance

    '''
    1 = not approve
    2 = approve
    '''

    def added_amount(self, instance=None):
        filter_u_wal = self.user_wallet_model.objects.get(
            user_id=instance.walletfinance.user_id
        )
        filter_u_wal.amount += float(instance.walletfinance.amount)
        filter_u_wal.save()

    def get(self, *args, **kwargs):
        model_id = self.kwargs.get('user_id')
        action_type_id = self.kwargs.get('type')
        if int(action_type_id) == 2:
            d = self.model.objects.filter(id=int(model_id))
            self.added_amount(instance=d.first())
            d.update(
                action_choice=int(action_type_id)
            )
        else:
            d = self.model.objects.filter(id=int(model_id))
            d.update(
                action_choice=1
            )
            w = self.walletfinance_model.objects.filter(id=d.first().walletfinance.id)
            w.update(
                list_display=True
            )
        return redirect('pendingdeposit')


class UserWithdrawAPIView(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)

    user_withdraw_model = UserWithdraw
    user_wallet_model = UserWallet

    def data_save_(self):
        a = IPTracker()
        return a.check_ip(self.request)

    def amount_debit(self, amount=None):
        a = self.user_wallet_model.objects.filter(user_id=self.request.user.id)
        amount_var = a.first().amount - amount
        if amount_var >= 0:
            a.update(
                amount=amount_var
            )
            return {'status': 0}
        return {'status': 1}

    def user_wallet_model_create(self, *args, **kwargs):
        data = self.data_save_()
        c = self.user_withdraw_model.objects.create(
            user_id=self.request.user.id,
            client_id=self.request.user.register.client_id,
            name=self.request.user.username,
            country=self.request.user.register.country,
            t_ip=data.get('ip'),
            t_country=data.get('country_name'),
            details="Withdraw Amount: {0}".format(self.request.data.get('amount')),
            currency="USD",
            amount=float(self.request.data.get('amount')),
            status=0,
            username=self.request.data.get('uname'),
            email=self.request.data.get('email')
        )
        c.save()
        a = self.amount_debit(float(self.request.data.get('amount')))
        if a['status'] == 1:
            c.details = "Withdraw not success: no balance"
            return {'status': 1}
        return {'status': 0}

    def post(self, *args, **kwargs):
        a = self.user_wallet_model_create()
        return Response(a)


class WithdrawApproveAPIView(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)

    '''
    Type: 1 => approve
    Type: 2 => cancel
    '''

    user_wallet_model = UserWallet
    user_withdraw_model = UserWithdraw

    def amount_added_on_wallet(self, instance_id, user_id):
        user_wallet_instance = self.user_wallet_model.objects.filter(user_id=user_id)
        if user_wallet_instance.exists():
            user_amount = user_wallet_instance.first().amount + self.user_withdraw_model.objects.get(id=instance_id).amount
            user_wallet_instance.update(
                amount=user_amount
            )
            return {'status': 0}
        return {'status': 1}

    def update_user_withdraw_model(self, instance_id, type):
        pass

    def get(self, *args, **kwargs):
        user_id = int(self.kwargs.get('user_id'))
        type = int(self.kwargs.get('type'))
        obj_id = int(self.kwargs.get('obj_id'))

        if type == 2:
            return_obj = self.amount_added_on_wallet(obj_id, user_id)
            if return_obj['status'] != 0:
                w_obj = self.user_withdraw_model.objects.filter(id=obj_id)
                w_obj.update(
                    detail="Not Wallet",
                    status=type
                )
            else:
                w_obj = self.user_withdraw_model.objects.filter(id=obj_id)
                w_obj.update(
                    status=type
                )
        w_obj = self.user_withdraw_model.objects.filter(id=obj_id)
        w_obj.update(
            status=type
        )
        return redirect('pendingwithdraw')


class AmountDashboardAPIView(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        user_id = self.request.user.id
        dashboard_data_deposit = self.dashboard_transaction_method.objects.filter(user_id=user_id, type=1)
        dashboard_data_withdraw = self.dashboard_transaction_method.objects.filter(user_id=user_id, type=2)
        return render(request, "amountdashboard.html", {"deposit": dashboard_data_deposit, "withdraw": dashboard_data_withdraw})
