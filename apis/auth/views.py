from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from clientportal.models import Uploaddocument, Client_Commission
from sportapp.models import (
    RegisterUserCampaign, Register
)
import requests
import json
import datetime
from common.models import (
    Country
)
from django.http import JsonResponse
from django.shortcuts import redirect, render
from clientportal.models import UserDepositApproval
from django.contrib.auth.models import User
from .serializers import (
    RegisterSerializer, SecurityqueModelSerializer, ClientMamabersListModelSerializer, IbWithdrawHistorySerializer,
    UserRegisterDataModelSerializer, RegisterClientModelSerializer, UpdatecampaignSerializer, RegisterUserCampaignModelSerializer,
    CountryModelSerializer, CommissionSerializer
)

from dashboard.models import (
    Securityque, Transaction_Method,transaction_ibmethod_mdl
)


class CommissionCreateAPI(CreateAPIView):
    queryset = Client_Commission.objects.all()
    serializer_class = CommissionSerializer


class ClientDetailAPIView(RetrieveAPIView):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer
    lookup_field = 'client_id'


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


class UserVerifiedAPIView(APIView):

    def get(self, *args, **kwargs):
        if self.request.user.profile.email_confirmed:
            return render_response(data="User's email is valid.", status=0, error=[])
        return render_response(data=[], status=1, error="user's email not verified.")


class GetUserDocApproveAPIView(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        if self.request.user.uploaddocument.approve:
            return render_response(data="Approved docs.", status=0)
        return render_response(status=1, error="Not approved docs.")


class ApproveDisapproveUserDocAPIView(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, *args, **kwargs):
        '''
        doc_id: is a Uploaddocument object id
        value: 0 is False and 1 is True
        '''
        value_var = True if int(self.kwargs.get('value', 0)) == 1 else False
        get_doc_upload_obj = Uploaddocument.objects.filter(id=self.kwargs.get('doc_id'))
        get_doc_upload_obj.update(approve=value_var)
        return render_response(data="User Doc status updated.", status=0)


class SaveCountryDataAPIView(APIView):
    authentication_classes = ()
    permission_classes = (AllowAny,)

    country_url = "https://restcountries.eu/rest/v2/all"

    def get(self, *args, **kwargs):
        r = requests.get(url=self.country_url)
        data = [i['name'] for i in json.loads(r.text)]
        for i in data:
            Country.objects.get_or_create(name=i)
        return render_response(data="Country data save.", status=0)


class UsersDepositApproveAPIView(APIView):
    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)

    user_deposit_approve_model = UserDepositApproval

    '''
    type: 1 (Approve), 2 (Disapprove)
    '''

    def get(self, *args, **kwargs):
        user_id = self.kwargs.get('user_id')
        type_id = self.kwargs.get('type')
        a = self.user_deposit_approve_model.objects.filter(user_id=int(user_id))
        if int(type_id) == 2 and a.exists():
            a.update(approve=False)
        else:
            obj, bool_var = self.user_deposit_approve_model.objects.get_or_create(user_id=int(user_id))
            if not bool_var:
                obj.approve = True
                obj.save()
        return redirect('client')

# class GetClientIdRefCampAPIView(APIView):
#     authentication_classes = ()
#     permission_classes = ()
#     serializers_var = RegisterModelSerializer
#     queryset_model = Register
#
#     def get(self, *args, **kwargs):
#         register_filter_obj = self.queryset_model.objects.filter(
#             client_id=self.kwargs.get('client_id')
#         )
#         if register_filter_obj.exists():
#             serializer_data = self.serializers_var(register_filter_obj.first())
#             return Response(
#                 {
#                     'data': serializer_data.data,
#                     'status': 0,
#                     'error': []
#                 }
#             )
#         return Response(
#             {
#                 'data': [],
#                 'status': 1,
#                 'error': 'No client id found'
#             }
#         )


class SecurityQueListAPIView(ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = SecurityqueModelSerializer
    queryset = Securityque.objects.all()


class SecurityQueListAPIView(ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = SecurityqueModelSerializer
    queryset = Securityque.objects.all()


class ClientMamabersListAPIView(ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ClientMamabersListModelSerializer
    queryset = RegisterUserCampaign.objects.all()

    def list(self, *args, **kwargs):
        client_id = self.kwargs.get('client_id')
        q = self.get_queryset().filter(register__client_id=client_id)
        return Response(self.serializer_class(q, many=True).data)


class UserRegisterDataListAPIView(ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserRegisterDataModelSerializer
    queryset = Register.objects.all()


class MamberClientDetailListAPIView(ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = RegisterClientModelSerializer
    queryset = RegisterUserCampaign.objects.all()

    def list(self, *args, **kwargs):
        q = self.get_queryset().filter(
            register__client_id=self.kwargs.get('client_id')
        )
        if q.exists():
            register_obj = Register.objects.filter(
                client_id=q.first().ref_code
            )
        if q.exists() and register_obj.exists():
            response_data = {
                'data': self.serializer_class(
                    register_obj.first()
                ).data,
                'status': 0,
                'error': ''
            }
        else:
            response_data = {
                'data': [],
                'status': 1,
                'error': 'not data found'
            }
        return Response(response_data)


class ClientMemberCountListAPIView(ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = ""
    queryset = RegisterUserCampaign.objects.all()

    def list(self, *args, **kwargs):
        q = self.get_queryset().filter(
            ref_code=self.kwargs.get('client_id')
        ).count()
        print('------------query set-----', q)
        return Response({'clients_count': q})


class CountryListAPIView(ListAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = CountryModelSerializer
    queryset = Country.objects.all()


class IbTransactionAPIView(ListAPIView):
    serializer_class = IbWithdrawHistorySerializer

    def get_queryset(self):
        client_id = self.kwargs['client_id']
        return transaction_ibmethod_mdl.objects.filter(client_id=client_id)


# class UpdatecampaignAPIView(UpdateAPIView):
#     serializer_class = UpdatecampaignSerializer
#     queryset = RegisterUserCampaign.objects.all()
#     lookup_field = 'ref_code'

def update_client_campaign(request, data):
    username, campaign_name = data.split('_')
    # print('Username and campaign_name ------->', username, campaign_name)
    RegisterUserCampaign.objects.filter(register__uname=username).update(campaign=campaign_name)
    return JsonResponse({
        'status': 'Updated'
    })


def get_client_campaign(request, username):
    qs = RegisterUserCampaign.objects.filter(register__uname=username).first()
    # print('qs---------------------------+++++++++++++++++++', qs)
    if qs:
        # print('enter in client_campign-------------------&&&&&&&&&')
        return JsonResponse({
            'campaign': qs.campaign
        })
    else:
        return JsonResponse({
            'campaign': 'no data available'
        })


class RegisterUserCampaignListAPIView(ListAPIView):

    authentication_classes = ()
    permission_classes = ()
    serializer_class = RegisterUserCampaignModelSerializer
    queryset = RegisterUserCampaign.objects.all()

from django.db.models import Sum
class AmountDashboardAPIView(APIView):

    authentication_classes = (SessionAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, **kwargs):

        deposit_days = int(request.GET.get('d1', '7'))
        withdraw_days = int(request.GET.get('d2', '7'))
        register_days = int(request.GET.get('d3', '7')) 
        d1_start = request.GET.get('d1start', 'null')
        d1_end = request.GET.get('d1end', 'null')
        d2_start = request.GET.get('d2start', 'null')
        d2_end = request.GET.get('d2end', 'null')
        d3_start = request.GET.get('d3start', 'null')
        d3_end = request.GET.get('d3end', 'null')

        today_date = datetime.datetime.today()
        start_date_deposit = today_date - datetime.timedelta(days=deposit_days-1)
        start_date_deposit = start_date_deposit.strftime("%Y-%m-%d")
        start_date_withdraw = today_date - datetime.timedelta(days=withdraw_days-1)
        start_date_withdraw = start_date_withdraw.strftime("%Y-%m-%d")
        start_date_register = today_date - datetime.timedelta(days=register_days-1)
        start_date_register = start_date_register.strftime("%Y-%m-%d")
        end_date_deposit = today_date
        end_date_withdraw = today_date
        end_date_register = today_date

        if d1_start != 'null' and d1_end != 'null':
            start_date_deposit = d1_start
            end_date_deposit = d1_end

        if d2_start != 'null' and d2_end != 'null':
            start_date_withdraw = d2_start
            end_date_withdraw = d2_end

        if d3_start != 'null' and d3_end != 'null':
            start_date_register = d3_start
            end_date_register = d3_end

        dashboard_data_deposit = Transaction_Method.objects.raw(f"SELECT id, DATE(added_on) as trans_date, Count(*) as count, SUM(amount) as amount_sum FROM dashboard_transaction_method WHERE type = '1' AND added_on BETWEEN '{start_date_deposit}' AND '{end_date_deposit}' GROUP BY DATE(added_on)")
        dashboard_data_withdraw = Transaction_Method.objects.raw(f"SELECT id,DATE(added_on) as trans_date, Count(*) as count, SUM(amount) as amount_sum FROM dashboard_transaction_method WHERE type = '2' AND added_on BETWEEN '{start_date_withdraw}' AND '{end_date_withdraw}' GROUP BY DATE(added_on)")
        dashboard_data_register = Register.objects.raw(f"SELECT id,DATE(added_on) as trans_date, Count(*) as count FROM sportapp_register WHERE added_on BETWEEN '{start_date_register}' AND '{end_date_register}' GROUP BY DATE(added_on)")

        values_deposit = []
        labels_deposit = []
        values_withdraw = []
        labels_withdraw = []
        values_register = []
        labels_register = []

        for dep in dashboard_data_deposit:
            values_deposit.append(dep.amount_sum)
            labels_deposit.append(dep.trans_date.strftime("%m-%d-%Y"))
        for wit in dashboard_data_withdraw:
            values_withdraw.append(wit.amount_sum)
            labels_withdraw.append(wit.trans_date.strftime("%m-%d-%Y"))
        for reg in dashboard_data_register:
            values_register.append(reg.count)
            # print("Values Regster---")
            labels_register.append(reg.trans_date.strftime("%m-%d-%Y"))

        return render(request, "dashboard/temp/amountdashboard.html", {"deposit": dashboard_data_deposit, "withdraw": dashboard_data_withdraw, "values_deposit": values_deposit, "labels_deposit": labels_deposit, "values_withdraw": values_withdraw, "labels_withdraw": labels_withdraw, "register": dashboard_data_register, "values_register": values_register, "labels_register": labels_register })
