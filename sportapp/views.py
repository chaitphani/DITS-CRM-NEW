from django.shortcuts import render,redirect,HttpResponse
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from clientportal.views import dashboard
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.db.models import Q
from django.contrib import auth
from django.contrib.auth.models import auth
from django.contrib.auth import get_user_model
from django.views.generic import View, TemplateView
from django.template.loader import render_to_string
from sportapp.tokens import account_activation_token
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from clientportal.models import UserWallet, LiveAccount
from dashboard.models import Securityque
from sport import settings

import math
import time
import random
import datetime
import requests, json

from .models import *

from django.db.models import Count, F, Value
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

User = get_user_model()


def home(request):

    auth.logout(request)
    return render(request,'home.html')


def tempAPI(request, mt4):

    _user = LiveAccount.objects.get(account_no=mt4)
    _u = Register.objects.get(user=_user.user)
    data = {'f_name': _u.fname, 'l_name': _u.lname, 'email': _u.email, 'clientId': _u.client_id}
    return JsonResponse(data)
   

def logout(request):

    auth.logout(request)
    return redirect('login_client')


# def user_mail_verify(request):

#     subject, from_email, to = 'hello', settings.EMAIL_HOST_USER, 'sandeepyadavjnp01@gmail.com'
#     text_content = Emailtemplate.objects.filter(t_type=1).first().template.format(username="Alex")

#     msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
#     msg.attach_alternative(text_content, 'text/html')
#     msg.send()
#     return HttpResponse("Hello")


# class VerifyUserToken(View):

#     def get(self, request, *args, **kwargs):

#         if 'user_id' and 'user_token' not in kwargs.keys():
#             return HttpResponse("Verify again your link is not valid")
            
#         get_user = User.objects.get(id=kwargs.get('user_id'))
#         check_user_token = account_activation_token.check_token(get_user, kwargs.get('user_token'))

#         if not check_user_token:
#             return HttpResponse("Your token invalid please send mail again.")
#         get_user_profile = Profile.objects.filter(user_id=kwargs.get('user_id'))

#         if not get_user_profile.exists():
#             return HttpResponse('User not exist in profile instnace.')

#         get_user_profile.update(email_confirmed=True)
#         return HttpResponse("Successfully verify your email.")


import requests
from django.conf import settings
from django.core.mail import EmailMessage

class UserSignupTemplateView(TemplateView):
    
    template_name = 'signup.html'

    # def country_api_call(self, *args, **kwargs):

    #     r = requests.get(url="http://api.countrylayer.com/v2/all?access_key=712d4a444d969c27f424f221f1f13213")
    #     #r = requests.get(url="https://restcountries.eu/rest/v2/all")
    #     c_data = [i['name'] for i in json.loads(r.text)]
    #     return c_data

    def get_context_data(self, *args, **kwargs):

        context = super(UserSignupTemplateView, self).get_context_data(**kwargs)
        context['sq'] = Securityque.objects.all()
        # context['country_names'] = self.country_api_call()
        context['cmp'] = self.request.GET.get('cmp')
        context['refid'] = self.request.GET.get('refid')

        return context

    def get(self, request, error=None, *args, **kwargs):

        context = self.get_context_data()
        if error:
            context['error'] = error
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        username_var = self.request.POST.get('uname')
        email_var = self.request.POST.get('email')
        pwd1 = request.POST.get('pwd1')
        pwd2 = request.POST.get('pwd2')

        if User.objects.filter(username=username_var).exists():
            messages.add_message(request, messages.ERROR, "Username has been already taken....!")
            return redirect('/signup')

        if User.objects.filter(email=email_var).exists():
            messages.add_message(request, messages.ERROR, "Email has been already taken....!")
            return redirect('/signup')

        if pwd1 != pwd2:
            messages.add_message(request, messages.ERROR, "Passwords Doesn't Match....!")
            return redirect('/signup')

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        uname = request.POST.get('uname')
        dob = request.POST.get('dob')
        email = request.POST.get('email')
        mob = request.POST.get('mob')
        campCode = request.POST.get('campCode', None)
        refid = request.POST.get('refid', None)
        country = request.POST.get('country')

        if Register.objects.all():
            last_user_client_id = Register.objects.last().client_id
            last_user_client_id += 1
        else:
            last_user_client_id = 1001

        user_obj = User.objects.create_user(username=username_var, password=pwd1, email=email_var)
        register = Register(fname=fname, client_id=last_user_client_id, lname=lname,uname=uname,dob=dob,email=email,mob=mob, country=country,pwd1=pwd1,pwd2=pwd2,user_id=user_obj.id)
                    # , acc_limit=4, demo_acc_limit=2)
        register.save()

        profile = Profile.objects.create(user_id=user_obj.id)
        user_wall = UserWallet.objects.create(user_id=user_obj.id, register_id=register.id)

        camp_data_api = requests.get(f'http://ib-admin.divsolution.com/api/v1/get-campaign-list').json()

        if campCode == None and refid == None:
            reg_user = RegisterUserCampaign.objects.create(register=register, ref_code=0, status=1)
            reg_user.save()
        else:
            res = {}
            for d in camp_data_api:
                res.update(d)
                if res['campaign_code'] == campCode:
                    camp_name = res['campaign_name'].strip()
                    reg_user_camp = RegisterUserCampaign.objects.create(ref_code=refid, campaign_code=campCode, register=register, campaign=camp_name, status=1)
                    reg_user_camp.save()

        subject = "Registration Successful.."
        body =  "Thank you for registering, your personal login information is as follows；\n\n"\
                "Client ID: \t{}".format(last_user_client_id)+'\n'+\
                "Username: \t{}".format(uname)+'\n'+\
                "Password: \t\t{}".format(pwd1)+'\n\n'+\
                "Every time you want to log in and manage your trading account, you need these login information, so please keep them in a safe place and don't provide them to anyone to avoid loss. \n"\
                "Log in to your client www.divsolution.com\n\n\n\n\n\n"\
                "Sincerely\n"\
                "DITS Team"

        from_email = settings.EMAIL_HOST_USER
        msg = EmailMessage(
            subject,
            body,
            from_email,
            [email],
            [from_email],
        )

        msg.send(fail_silently=False)
        return redirect('login_client')


from .forms import CodeVerificationForm
from django.contrib.auth import authenticate,login
from django.shortcuts import get_object_or_404
from django.contrib.auth import logout as auth_logout


def code_verification(request):

    message = None
    Verification_Code = request.session.get('verificationcode',False)
    if request.method == 'POST':
        form = CodeVerificationForm(request.POST)
        code = request.POST.get('code')
        if form.is_valid():
            if code==Verification_Code:
                Register.objects.filter(user=request.user).update(verify=True)
                auth_logout(request)
                return redirect(logins)
            else:
                message = 'Code Eneterd is wrong'
        else:
            print(form.errors)
    else:
        form = CodeVerificationForm()
    return render(request,'code_verification.html',{'Verification_Code':Verification_Code,'message':message,'form':form})


def about(request):
    return render(request,'about.html')

def assets(request):
    return render(request,'asset.html')

def platform(request):
    return render(request,'platforms.html')

def withdraw(request):
    return render(request,'withdraw.html')

def deposit(request):
    return render(request,'deposit.html') 

def partner(request):
    return render(request,'partener.html') 


# from django.forms import ModelForm
# class ContactForm(ModelForm):
#     class Meta:
#         model = Contact
#         fields = '__all__'

from .models import Contact
def contact(request):

    if request.method =="POST":

        lname = request.POST.get('lname')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        cmt = request.POST.get('cmt')
        contact = Contact.objects.create(fname='some', lname=lname, phone=phone, email=email, cmt=cmt)
        contact.save()
        messages.success(request, 'Thank You! Our support team will contact you soon.')
        # return redirect('home')

    return render(request,'contact.html')


def logins(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['pwd']
        register = auth.authenticate(username=username,password=password)
        if register is not None:
            auth.login(request,register)
            # return redirect('profile')
            return redirect('profile')
        else:
            return render(request,'login.html',{'error':'Invalid Login Credentials'})
    else:
        context_data={
            'u':User.objects.all()
        }
        return render(request, 'login.html', context_data)


# API views for IB's
from datetime import datetime, timedelta
from clientportal.models import LiveAccount
def trades_data(request):

    ib_users_res_json={}

    resp = []

    category_url = f'{settings.IB_ADMIN}/api/v1/get-lot-category'
    category_res = requests.get(category_url)
    category_json = category_res.json()

    reg_user_campain_obj = RegisterUserCampaign.objects.filter().annotate(
        uname = F('register__uname'),
        email = F('register__email'),
    )

    ib_id =request.GET.get('ib_id', '')

    ib_user_url = f"{settings.IB_URL}/api/v1/ib_users/{ib_id}"

    ib_users_res = requests.get(ib_user_url)
    if ib_users_res.status_code == 200:
        ib_users_res_json = ib_users_res.json()

    each_ib_user=ib_users_res_json

    register_objs = Register.objects.filter(registerusercampaign__ref_code=ib_id, registerusercampaign__status=1).annotate(
        campaign = F('registerusercampaign__campaign'),
        ref_code = F('registerusercampaign__ref_code'),
        reg_id = F('registerusercampaign__register_id'),
        name = F('uname'),
        login = F('registerusercampaign__mt4_id'),
        updated_on_ = F('registerusercampaign__updated_on')
    )

    for each_robj in register_objs:

        url = f"{settings.IB_ADMIN}/api/v1/get_campaign_code/{each_ib_user['ib_id']}"
        res = requests.get(url)

        if res.status_code == 200:
            res_json = res.json()

        mtu_data = Mt4users.objects.filter(login=each_robj.login)

        for each_mtu in mtu_data:
            import datetime
            mtt_data = Mt4trades.objects.filter(login=each_mtu.login, open_time__gte=each_robj.added_on).exclude(symbol__exact='')

            for each_mtt in mtt_data:

                open_time_split = datetime.datetime.strftime(each_mtt.open_time, "%d-%m-%Y %H:%M:%S")
                close_time_split = datetime.datetime.strftime(each_mtt.close_time, "%d-%m-%Y %H:%M:%S")

                commission = None
                resp.append(
                    {"mt4_acc":each_mtt.login, "symbol":each_mtt.symbol, 
                    "open_time":open_time_split, 
                    "close_time":close_time_split,
                    "profit":each_mtt.profit, "status":each_mtt.status, 
                    "reg_id":each_robj.reg_id, "name":each_mtu.name, 
                    "volume":(each_mtt.volume)/100, "balance":each_mtu.balance}
                )

                lot_name = [category['category']['c_name'] for category in category_json if category['sub_name'] == each_mtt.symbol]

                if lot_name:
                    lot_name = lot_name[0]
                    if ' ' in lot_name:
                        lot_name = '_'.join(lot_name.split())

                    # campaign_name = each_robj.campaign
                        # for campaign_details in res_json['campaign_code']:
                        #     if campaign_details['campaign_name'].strip() == campaign_name.strip():
                        #         campaign = campaign_details 
                        #         break

                    try:
                        volume = (each_mtt.volume)/100
                        lot_value = res_json["campaign_code"][0].get(lot_name.lower()) if res_json["campaign_code"][0] else None 
                        if lot_value:
                            commission = volume * lot_value

                            # if r_list[-1] == '0':
                            #     client_commission[r_list[1]]['commision_unpaid'].append(commission)
                            # else:
                            #     client_commission[r_list[1]]['commision_paid'].append(commission)
                        else:
                            commission = None
                    except:
                        pass
                else:
                    commission = None

                # commision = each_mtt.volume/100
                # fx_value = 0
                # if(each.campaign != None):
                #     fx_value = int(each.campaign[3])

                if int(each_mtt.status) == 0:
                    commission= commission
                else:
                    commission = 'Paid'

                resp[-1]["commission"] = commission

    return JsonResponse(resp, safe=False)


def clients_data(request):

    resp = []   
    
    category_url = f'{settings.IB_ADMIN}/api/v1/get-lot-category'

    category_res = requests.get(category_url)
    category_json = category_res.json()

    ib_id = request.GET.get('ib_id', '')

    ib_user_url = f"{settings.IB_URL}/api/v1/ib_users/{ib_id}"
    ib_users_res = requests.get(ib_user_url)
    ib_users_res_json={}

    if ib_users_res.status_code == 200:
        ib_users_res_json = ib_users_res.json()

    each_ib_user=ib_users_res_json

    register_objs = Register.objects.filter(registerusercampaign__ref_code=ib_id, registerusercampaign__status=1).annotate(
        campaign = F('registerusercampaign__campaign'),
        ref_code = F('registerusercampaign__ref_code'),
        reg_id = F('registerusercampaign__register_id'),
        name = F('uname'),
        status = F('registerusercampaign__status'),
        login = F('registerusercampaign__mt4_id'),
        updated_on_ = F('registerusercampaign__updated_on'),
    )

    try:
        ib_id = each_ib_user['ib_id']
    except:
        ib_id = ''

    url = f"{settings.IB_ADMIN}/api/v1/get_campaign_code/{ib_id}"

    res = requests.get(url)
    if res.status_code == 200:
        res_json = res.json()

    for each_robj in register_objs:

        mtu_data = Mt4users.objects.filter(login=each_robj.login)

        if(len(mtu_data) == 0):
            resp.append({
                "mt4_acc":0,
                "username":each_robj.uname,
                "email":each_robj.email,
                "balance":0,
                "withdraw":0,
                "deposit":0,
                "campaign":each_robj.campaign,
                "volumetraded":0,
                "commission_paid":0,
                "commission_unpaid":0,
                'status':each_robj.status,
            })

        for each_mtu in mtu_data:
            BALANCE = each_mtu.balance
            COMMISION_PAID = 0
            COMMISSION_UNPAID = 0
            VOLUME_TRADED = 0
            DEPOSIT = 0
            WITHDRAW = 0

            mtt_no_symbol_data = Mt4trades.objects.filter(login=each_mtu.login, open_time__gte=each_robj.updated_on_ + timedelta(hours=3)).filter(symbol='')
            for each_mtt_no_symbol in mtt_no_symbol_data:

                if int(each_mtt_no_symbol.profit) < 0:
                    WITHDRAW = WITHDRAW + float(each_mtt_no_symbol.profit)
                else:
                    DEPOSIT = DEPOSIT + float(each_mtt_no_symbol.profit)

            mtt_data = Mt4trades.objects.filter(login=each_mtu.login, open_time__gte=each_robj.updated_on_ + timedelta(hours=3)).exclude(symbol__exact='')

            for each_mtt in mtt_data:
                commission = 0
                VOLUME_TRADED = VOLUME_TRADED + float(each_mtt.volume)/100

                lot_name = [category['category']['c_name'] for category in category_json if category['sub_name'] == each_mtt.symbol]

                if lot_name:
                    lot_name = lot_name[0]
                    if ' ' in lot_name:
                        lot_name = '_'.join(lot_name.split()) 

                    # campaign_name = each_robj.campaign
                    try:
                        volume = (each_mtt.volume)/100
                        lot_value = res_json["campaign_code"][0].get(lot_name.lower()) if res_json["campaign_code"][0] else None 
                        if lot_value:
                            commission = volume * lot_value

                                    # May b this can be commented..
                            # if r_list[-1] == '0':
                            #     client_commission[r_list[1]]['commision_unpaid'].append(commission)
                            # else:
                            #     client_commission[r_list[1]]['commision_paid'].append(commission)
                        else:
                            commission = 0
                    except:
                        pass
                else:
                    commission = 0

                if int(each_mtt.status) == 0:
                    COMMISSION_UNPAID = float(COMMISSION_UNPAID) + float(commission)
                else:
                    COMMISION_PAID = float(COMMISION_PAID) + float(commission)

            resp.append({"mt4_acc":each_mtu.login, "username":each_mtu.name, "email":each_mtu.email, "balance":BALANCE, "commission_paid":COMMISION_PAID,"commission_unpaid":COMMISSION_UNPAID, "volumetraded":VOLUME_TRADED, "campaign":each_robj.campaign, "deposit":DEPOSIT, "withdraw":WITHDRAW,'status':each_robj.status})

    return JsonResponse(resp, safe=False)

# import datetime
@csrf_exempt
def assignIBToClient(request):

    campaign_name = ''
    campaign_code = ''

    if request.method == 'POST':
        try:
            login = request.POST.get('login')
            ib_id = request.POST.get('ib_id')
            campaigns = request.POST.get('campaigns')
            txt_email = request.POST.get('txt_email')

            url = f'{settings.IB_ADMIN}/api/v1/get-campaign-list'
            json_data = requests.get(url).json()

            for data in json_data:
                if int(data['id']) == int(campaigns):
                    campaign_name = data['campaign_name']
                    campaign_code = data['campaign_code']

            mtu_obj = Mt4users.objects.get(login=login)
            reg_obj = Register.objects.filter(uname=mtu_obj.name).first()
            # reg_camp_obj = RegisterUserCampaign.objects.filter(register_id=reg_obj.id, mt4_id=login)
            reg_camp_obj = RegisterUserCampaign.objects.filter(register=reg_obj, mt4_id=login, status=1)

            if(len(reg_camp_obj) > 0 and reg_camp_obj.first().ref_code != '' and reg_camp_obj.first().ref_code != 0):
                return JsonResponse({'msg':'Already Client assigned for this IB'}, status=401)

            cls_time_list = []
            mt4_trade_obj = Mt4trades.objects.filter(login=mtu_obj.login)
            trade_obj = mt4_trade_obj.values('close_time')

            for cls_time in trade_obj:
                convert = cls_time['close_time'].strftime("%Y-%m-%d %H:%M:%S")
                if convert == '1970-01-01 00:00:00':
                    cls_time_list.append(convert)

            # reg_user_exists = RegisterUserCampaign.objects.filter(mt4_id=login, status=1, register=reg_obj)
            # if not len(reg_user_exists) > 1:
            if txt_email == reg_obj.email:
                if not len(cls_time_list) != 0:
                    reg_camp_obj.update(ref_code=ib_id, campaign=campaign_name, campaign_code=campaign_code, updated_on=datetime.now())
                else:
                    return JsonResponse({'msg':'Trade is running you can not add client..'}, safe=False, status=402)
            else:
                return JsonResponse({'msg':'Please provide valid details to add..'}, safe=False, status=400)
            # else:
            #     return JsonResponse({'msg':'client already exists with same IB...'}, safe=False, status=304)

        except Exception as e:
            print('-------exception----', e)
            return JsonResponse({'msg':str(e)}, safe=False, status=403)
        return JsonResponse({'msg':'Data updated successfully'}, safe=False, status=200)
    return JsonResponse({}, safe=False)


@csrf_exempt
def transferClient(request):

    campaign_name = ''
    campaign_code = ''

    if request.method == 'POST':
        try:
            ib_id = request.POST.get('ib_id')
            campaigns = request.POST.get('campaigns')
            login = request.POST.get('login')

            # url_1 = f'{settings.IB_ADMIN}/api/v1/get_campaign_code/{ib_id}'
            # json_check = requests.get(url_1).json()['campaign_code']

            # id_list=[]
            # for data in json_check:
            #     id_list.append(int(data['id']))

            url = f'{settings.IB_ADMIN}/api/v1/get-campaign-list'
            json_data = requests.get(url).json()

            for data in json_data:
                if int(data['id']) == int(campaigns):
                    campaign_name = data['campaign_name']
                    campaign_code = data['campaign_code']

            mtu_obj = Mt4users.objects.get(login=login)
            reg_obj = Register.objects.get(uname=mtu_obj.name)

            try:
                user_exist_with_same = RegisterUserCampaign.objects.get(register_id=reg_obj.id, status=1, mt4_id=login, ref_code=ib_id)
                if user_exist_with_same:
                    return JsonResponse({'msg':'Client already with same IB..'}, safe=False, status=401)
            except Exception as e:
                print('---exception in upper trasfer---', e)
                pass

            cls_time_list = []
            mt4_trade_obj = Mt4trades.objects.filter(login=mtu_obj.login)
            trade_obj = mt4_trade_obj.values('close_time')

            for cls_time in trade_obj:
                convert = cls_time['close_time'].strftime("%Y-%m-%d %H:%M:%S")
                if convert == '1970-01-01 00:00:00':
                    cls_time_list.append(convert)
    
            mt4_trades_obj = Mt4trades.objects.filter(login=mtu_obj.login).last()

            if mt4_trades_obj:
                if not len(cls_time_list) != 0:
                    if int(mt4_trades_obj.status) == 1 or mt4_trades_obj.symbol == '':
                        reg_camp_obj = RegisterUserCampaign.objects.get(register_id=reg_obj.id, status=1, mt4_id=login)

                        reg_camp_obj.status = 0
                        reg_camp_obj.save()

                        reg_camp_obj.id = None
                        reg_camp_obj.ref_code = ib_id

                        reg_camp_obj.campaign = campaign_name
                        reg_camp_obj.campaign_code = campaign_code
                        reg_camp_obj.status = 1
                        reg_camp_obj.updated_on = datetime.now()
                        # print('---suceess--------')
                        reg_camp_obj.save()
                    else:
                        return JsonResponse({'msg':'Commission unpaid, Can not transfer this client...'}, safe=False, status=402)
                else:
                    return JsonResponse({'msg':'Trade running, can not transfer.....'}, safe=False, status=406)
            else:
                return JsonResponse({'msg':'No trades data found for the provided login number.....'}, safe=False, status=405)

        except Exception as e:
            print('-exception as error------', e)
            return JsonResponse({'msg':str(e)}, safe=False, status=502)
        return JsonResponse({'msg':'Data updated successfully'}, safe=False, status=200)
    return JsonResponse({}, safe=False)   


def getIBAdminAndIBPortalCumulativeData(request):

    ib_users_res_json={}
    resp = []

    category_url = f'{settings.IB_ADMIN}/api/v1/get-lot-category'
    category_res = requests.get(category_url)
    category_json = category_res.json()

    reg_user_campain_obj = RegisterUserCampaign.objects.filter().annotate(
        uname = F('register__uname'),
        email = F('register__email'),
    )

    ib_id =request.GET.get('ib_id', '')

    ib_user_url = f"{settings.IB_URL}/api/v1/ib_users"
    
    if(ib_id != ''):
        ib_user_url = f"{settings.IB_URL}/api/v1/ib_users/{ib_id}"  

    ib_users_res = requests.get(ib_user_url)
    if ib_users_res.status_code == 200:
        ib_users_res_json = ib_users_res.json()

    each_ib_user=ib_users_res_json

    if(ib_id != ''):
        each_ib_user=[ib_users_res_json]

    ib_ids_list = []
    comm_paid = []
    for each_ib in each_ib_user:
        ib_ids_list.append(each_ib['ib_id'])
        check_ib = each_ib['ib_id']
        url = f'{settings.IB_URL}/api/v1/client_commission/{check_ib}'
        json_url_data = requests.get(url).json()

        try:
            comm_paid.append(json_url_data['commision_paid'])
        except:
            pass

    reg_user_camp_obj=RegisterUserCampaign.objects.filter(ref_code__in=ib_ids_list, status=1).annotate(
        login = F('mt4_id'),
        reg_id = F('register_id'),
        name = F('register__uname'),
        updated_on_ = F('updated_on'),
    )

    response = {
        "balance":0,
        "withdraw":0,
        "deposit":0,
        "volumetraded":0,
        "commission_paid":sum(comm_paid),
        "commission_unpaid":0,
        "clients":0,
        "accounts":len(reg_user_camp_obj)
    }

    print('-------reg user camp obj--------', reg_user_camp_obj)

    clients_list = []
    for each_robj in reg_user_camp_obj:
        print('-----each robj---------', each_robj)
        # print('-----each robj---------', each_robj.username)
        print('-----each robj---------', each_robj.register.email)

        if(each_robj.register.email not in clients_list):
            clients_list.append(each_robj.register.email)

        url = f"{settings.IB_ADMIN}/api/v1/get_campaign_code/{each_robj.ref_code}"

        res = requests.get(url)
        if res.status_code == 200:
            res_json = res.json()

        mtu_data = Mt4users.objects.filter(login=each_robj.login)

        for each_mtu in mtu_data:
            response["balance"] = float(response["balance"]) + float(each_mtu.balance)

            mtt_data_no_symbol = Mt4trades.objects.filter(login=each_mtu.login, open_time__gte=each_robj.updated_on_ + timedelta(hours=3)).filter(symbol='')

            for each_mtt_no_symbol in mtt_data_no_symbol:
                if float(each_mtt_no_symbol.profit) < 0:
                    response["withdraw"] = float(response["withdraw"]) + float(each_mtt_no_symbol.profit)
                else:
                    response["deposit"] = float(response["deposit"]) + float(each_mtt_no_symbol.profit)

            mtt_data = Mt4trades.objects.filter(login=each_mtu.login, open_time__gte=each_robj.updated_on_ + timedelta(hours=3)).exclude(symbol__exact='')

            for each_mtt in mtt_data:

                commission = 0
                response['volumetraded'] = float(response['volumetraded']) + float(each_mtt.volume)/100
            
                lot_name = [category['category']['c_name'] for category in category_json if category['sub_name'] == each_mtt.symbol]

                if lot_name:
                    lot_name = lot_name[0]

                    if ' ' in lot_name:
                        lot_name = '_'.join(lot_name.split())
                    try:
                        volume = float(each_mtt.volume)/100
                        lot_value = res_json["campaign_code"][0].get(lot_name.lower()) if res_json["campaign_code"][0] else None

                        if lot_value:
                            commission =  volume * lot_value
                        else:
                            commission = 0
                    except:
                        pass
                else:
                    commission = 0

                if int(each_mtt.status) != 0:
                    response["commission_paid"] = float(response["commission_paid"]) + float(commission)
                else:
                    response["commission_unpaid"] = float(response["commission_unpaid"]) + float(commission)


    response["clients"] = len(clients_list)
    response["clients_list"] = clients_list

    return JsonResponse(response, safe=False)


def VolumeCumulativeData(request):

    ib_users_res_json={}
    resp = []
    reg_camp_id_list = []
    category_url = f'{settings.IB_ADMIN}/api/v1/get-lot-category'
    category_res = requests.get(category_url)
    category_json = category_res.json()

    ib_id =request.GET.get('ib_id', '')

    ib_user_url = f"{settings.IB_URL}/api/v1/ib_users"
    
    if(ib_id != ''):
        ib_user_url = f"{settings.IB_URL}/api/v1/ib_users/{ib_id}"  

    ib_users_res = requests.get(ib_user_url)
    if ib_users_res.status_code == 200:
        ib_users_res_json = ib_users_res.json()

    each_ib_user=ib_users_res_json

    if(ib_id != ''):
        each_ib_user=[ib_users_res_json]

    ib_ids_list = []
    comm_paid = []

    for each_ib in each_ib_user:
        ib_ids_list.append(each_ib['ib_id'])
        check_ib = each_ib['ib_id']
        url = f'{settings.IB_URL}/api/v1/client_commission/{check_ib}'
        json_url_data = requests.get(url).json()

        try:
            comm_paid.append(json_url_data['commision_paid'])
        except:
            pass

    # reg_user_camp_obj=RegisterUserCampaign.objects.filter(ref_code__in=ib_ids_list).annotate(
    #     login = F('mt4_id'),
    #     reg_id = F('register_id'),
    #     name = F('register__uname'),
    #     updated_on_ = F('updated_on'),
    # )

    # reg_status_obj=RegisterUserCampaign.objects.filter(ref_code__in=ib_ids_list, status=1).annotate(
    #     login = F('mt4_id'),
    #     reg_id = F('register_id'),
    #     name = F('register__uname'),
    #     updated_on_ = F('updated_on'),
    # ).last()

    response = {
        # "balance":0,
        "withdraw":0,
        "deposit":0,
        "volumetraded":0,
        "commission_paid":round(sum(comm_paid), 2),
        "commission_unpaid":0,
        # "clients":0,
        # "accounts":len(reg_user_camp_obj)
    }

    for each_ib in ib_ids_list:

        reg_user_camp_obj=RegisterUserCampaign.objects.filter(ref_code=each_ib).annotate(
        login = F('mt4_id'),
        reg_id = F('register_id'),
        name = F('register__uname'),
        updated_on_ = F('updated_on'),
        )
        url = f"{settings.IB_ADMIN}/api/v1/get_campaign_code/{each_ib}"

        res = requests.get(url)
        if res.status_code == 200:
            res_json = res.json()

        for each_robj in reg_user_camp_obj:

            # if each_robj.login not in reg_camp_id_list:
            #     reg_camp_id_list.append(each_robj.login)
            try:
                mtu_data = Mt4users.objects.get(login=each_robj.login)
            except Exception as e:
                print('--------exception as error----------', e)
                return Respone({'msg':'No user found with this login'}, status=400)
                #  (or) multiple users found with this login'}, status=400)

            # response["balance"] = float(response["balance"]) + float(mtu_data.balance)
            mtt_data_no_symbol = None

            if(each_robj.status==0):
                mtt_data_no_symbol = Mt4trades.objects.filter(login=each_robj.login, open_time__gte=each_robj.added_on + timedelta(hours=3), open_time__lt=each_robj.updated_on + timedelta(hours=3)).filter(symbol='')
            else:
                 mtt_data_no_symbol = Mt4trades.objects.filter(login=each_robj.login, open_time__gte=each_robj.updated_on + timedelta(hours=3)).filter(symbol='')

            for each_mtt_no_symbol in mtt_data_no_symbol:
                # if(each_robj.status == 1):
                if float(each_mtt_no_symbol.profit) < 0:
                    response["withdraw"] = float(response["withdraw"]) + float(each_mtt_no_symbol.profit)
                else:
                    response["deposit"] = float(response["deposit"]) + float(each_mtt_no_symbol.profit)

            mtt_data = None

            if(each_robj.status==0):
                mtt_data = Mt4trades.objects.filter(login=each_robj.login, open_time__gte=each_robj.added_on + timedelta(hours=3), open_time__lt=each_robj.updated_on + timedelta(hours=3)).exclude(symbol__exact='')
            else:
                 mtt_data = Mt4trades.objects.filter(login=each_robj.login, open_time__gte=each_robj.updated_on + timedelta(hours=3)).exclude(symbol__exact='')       

            for each_mtt in mtt_data:
                if each_mtt.ticket not in reg_camp_id_list:
                    reg_camp_id_list.append(each_mtt.ticket)

                    commission = 0
                    response['volumetraded'] = float(response['volumetraded']) + float(each_mtt.volume)/100

                    lot_name = [category['category']['c_name'] for category in category_json if category['sub_name'] == each_mtt.symbol]

                    if lot_name:
                        lot_name = lot_name[0]

                        if ' ' in lot_name:
                            lot_name = '_'.join(lot_name.split())
                        try:
                            volume = float(each_mtt.volume)/100
                            lot_value = res_json["campaign_code"][0].get(lot_name.lower()) if res_json["campaign_code"][0] else None

                            if lot_value:
                                commission =  volume * lot_value
                            else:
                                commission = 0
                        except:
                            pass
                    else:
                        commission = 0

                    if int(each_mtt.status) != 0:
                        response["commission_paid"] = float(response["commission_paid"]) + float(commission)
                    else:
                        response["commission_unpaid"] = float(response["commission_unpaid"]) + float(commission)

        # response["clients"] = len(clients_list)
        # response["clients_list"] = clients_list

    return JsonResponse(response, safe=False)


def payments_data(request):

    resp = []   
    
    category_url = f'{settings.IB_ADMIN}/api/v1/get-lot-category'

    category_res = requests.get(category_url)
    category_json = category_res.json()

    ib_id = request.GET.get('ib_id', '')

    ib_user_url = f"{settings.IB_URL}/api/v1/ib_users/{ib_id}"
    ib_users_res = requests.get(ib_user_url)
    ib_users_res_json={}

    if ib_users_res.status_code == 200:
        ib_users_res_json = ib_users_res.json()

    each_ib_user=ib_users_res_json
    
    register_objs = Register.objects.filter(registerusercampaign__ref_code=ib_id, registerusercampaign__status=1).annotate(
        campaign = F('registerusercampaign__campaign'),
        ref_code = F('registerusercampaign__ref_code'),
        reg_id = F('registerusercampaign__register_id'),
        name = F('uname'),
        status = F('registerusercampaign__status'),
        login = F('registerusercampaign__mt4_id'),
        updated_on_ = F('registerusercampaign__updated_on'),
    )
    try:
        ib_id = each_ib_user['ib_id']
    except:
        ib_id = ''

    url = f"{settings.IB_ADMIN}/api/v1/get_campaign_code/{ib_id}"

    res = requests.get(url)
    if res.status_code == 200:
        res_json = res.json()

    for each_robj in register_objs:
        mtu_data = Mt4users.objects.filter(login=each_robj.login)
        if(len(mtu_data) == 0):
            resp.append({
                "username":each_robj.uname,
                "email":each_robj.email,
                "commission_unpaid":0,
            })

        for each_mtu in mtu_data:
            COMMISSION_UNPAID = 0
            mtt_data = Mt4trades.objects.filter(login=each_mtu.login, open_time__gte=each_robj.updated_on_).exclude(symbol__exact='')
            for each_mtt in mtt_data:
                commission = 0
                lot_name = [category['category']['c_name'] for category in category_json if category['sub_name'] == each_mtt.symbol]
                if lot_name:
                    lot_name = lot_name[0]
                    if ' ' in lot_name:
                        lot_name = '_'.join(lot_name.split()) 
                    try:
                        volume = (each_mtt.volume)/100
                        lot_value = res_json["campaign_code"][0].get(lot_name.lower()) if res_json["campaign_code"][0] else None 
                        if lot_value:
                            commission = volume * lot_value
                        else:
                            commission = 0
                    except:
                        pass
                else:
                    commission = 0
                if int(each_mtt.status) == 0:
                    COMMISSION_UNPAID = float(COMMISSION_UNPAID) + float(commission)
                # else:
                #     print('paid')
                #     COMMISION_PAID = float(COMMISION_PAID) + float(commission)

            resp.append({"ib_id":ib_id, "username":each_ib_user['uname'], "email":each_ib_user['email'],"commission_unpaid":COMMISSION_UNPAID})

    return JsonResponse(resp, safe=False)


def proceed_payout(request):

    login = request.GET.get('login', '')
    ib_id = request.GET.get('ib_id', '')

    # if(ib_id != ''):
    #   ib_user_url = f"{settings.IB_URL}/api/v1/ib_users/{ib_id}"  

    # ib_users_res = requests.get(ib_user_url)
    # if ib_users_res.status_code == 200:
    #     ib_users_res_json = ib_users_res.json()

    # each_ib_user=ib_users_res_json

    # if(ib_id != ''):
    #     each_ib_user=[ib_users_res_json]

    # ib_ids_list = []
    # for each_ib in each_ib_user:
    #     ib_ids_list.append(each_ib['ib_id'])

    # for each_robj in reg_user_camp_obj:
        # for each_mtu in mtu_data:
    # try:
        # update_obj = Mt4trades.objects.filter(login=login).update(status=1)
    # except:
            # return JsonResponse({'msg':'No data found with the MT4 login...'}, safe=False, status=401)

    try:
        # print('---inside try block---------')
        # print('-----reg camp user obj---------', reg_user_camp_obj)
        # print('-----mtu data with teh login------', mtu_data)
        # print('---inside if cond of len cehck with regcamp and mt4users')

        reg_user_camp_obj=RegisterUserCampaign.objects.filter(mt4_id=login, status=1, ref_code=ib_id)

        mtu_data = Mt4users.objects.filter(login=login)

        if len(reg_user_camp_obj) > 0 and len(mtu_data) > 0:

            mt4_trade_obj = Mt4trades.objects.filter(login=login)
            trade_obj = mt4_trade_obj.values('close_time')

            cls_time_list = []
            for cls_time in trade_obj:
                convert = cls_time['close_time'].strftime("%Y-%m-%d %H:%M:%S")
                if convert == '1970-01-01 00:00:00':
                    cls_time_list.append(convert)

            if not len(cls_time_list) != 0:
                update_obj = Mt4trades.objects.filter(login=login).update(status=1)
                # print('-------status changed sucess-------')
            else:
                return JsonResponse({'msg':'Trade is running, can not process the request..'}, safe=False, status=401)
        else:
            return JsonResponse({'msg':'No user found with the provided data...'}, safe=False, status=402)
    except Exception as e:
        print('-----exceptio as error-------', e)
        return JsonResponse({'msg':'Unable to find the data for the user provided..'}, safe=False, status=403)

    return JsonResponse({}, safe=False)
