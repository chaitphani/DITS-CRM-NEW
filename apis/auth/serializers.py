from rest_framework import serializers
from clientportal.models import Client_Commission
from common.models import (
    Country
)
from sportapp.models import (
    RegisterUserCampaign,Register
)
from django.urls import reverse
from django.conf import settings
from dashboard.models import (
    Securityque,Comments,Addcurrency,transaction_ibmethod_mdl
)

class RegisterSerializer(serializers.ModelSerializer):
    # campaign_code = serializers.SerializerMethodField()
    # ref = serializers.SerializerMethodField()
    # link = serializers.SerializerMethodField()
    # partner_id = serializers.SerializerMethodField()

    class Meta:
        model = Register
        fields = '__all__'
#
    # def get_campaign_code(self, obj):
    #     # return obj.user_campaign_code
    #     return "al"
    #
    # def get_ref(self, obj):
    #     return obj.client_id
    #
    # def get_link(self, obj):
    #     link_var = settings.CLIENTPORTAL_LINK + "{0}?camp={1}&ref={2}".format(
    #         reverse('signup'),
    #         # obj.user_campaign_code,
    #         "a",
    #         obj.client_id
    #     )
    #     return link_var
    #
    # def get_partner_id(self, obj):
    #     try:
    #         a = obj.registerusercampaign_set.first().ref_code
    #     except:
    #         a = None
    #     return a

class SecurityqueModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Securityque
        fields = ['name']

class ClientRegisterModelSerializerExclude(serializers.ModelSerializer):
    live_account = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Register
        exclude = ['pwd1', 'pwd2', 'user', 'id', 'object_status',
                    'updated_on', 'verify', 'added_on', ]

    def get_live_account(self, obj):
        try:
            a = obj.user.liveaccount_set.first().account_no
        except Exception as e:
            print(e)
            a = None
        return a

class ClientMamabersListModelSerializer(serializers.ModelSerializer):
    partner_id = serializers.SerializerMethodField(read_only=True)
    register = ClientRegisterModelSerializerExclude()

    class Meta:
        model = RegisterUserCampaign
        exclude = ['added_on', 'updated_on', 'id', 'object_status', 'ref_code']
        depth = 1

    def get_partner_id(self, obj):
        return obj.ref_code

class RegisterUserCampaignModelSerializer(serializers.ModelSerializer):
    partner_name = serializers.SerializerMethodField(read_only=True)

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(RegisterUserCampaignModelSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

    class Meta:
        model = RegisterUserCampaign
        # fields = '__all__'
        exclude = ['register', 'campaign_code', 'updated_on']
        extra_fields = ['partner_name']

    def get_partner_name(self, obj):
        return Register.objects.get(client_id = obj.ref_code).uname

class UserRegisterDataModelSerializer(serializers.ModelSerializer):
    # partner = serializers.SerializerMethodField(read_only=True)

    # def get_field_names(self, declared_fields, info):
    #     expanded_fields = super(UserRegisterDataModelSerializer, self).get_field_names(declared_fields, info)
    #
    #     if getattr(self.Meta, 'extra_fields', None):
    #         return expanded_fields + self.Meta.extra_fields
    #     else:
    #         return expanded_fields

    class Meta:
        model = Register
        fields = '__all__'
        # exclude = ['pwd1', 'pwd2', 'user', 'id', 'object_status',
                    # 'updated_on', 'verify', 'added_on', 'sque', 'sans']
        # extra_fields = ['partner']

    # def get_partner(self, obj):
    #     a = RegisterUserCampaign.objects.filter(register_id = obj.id)
    #     if a.exists():
    #         return RegisterUserCampaignModelSerializer(a.first()).data
    #     return ""

class CommonExtraFieldModelSerializer(serializers.ModelSerializer):
    def get_field_names(self, declared_fields, info):
        expanded_fields = super(CommonExtraFieldModelSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

class RegisterClientModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        exclude = ['pwd1', 'pwd2', 'user', 'id', 'object_status',
                    'updated_on', 'verify', 'added_on', 'sque', 'sans',
                    "reasonsecondaryemail", "secondaryemail"]

class CountryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        exclude = ['slug', 'id']
#
class CommissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client_Commission
        fields = '__all__'

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class AddCurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Addcurrency
        fields = '__all__'

class IbWithdrawHistorySerializer(serializers.ModelSerializer):
    comments = CommentsSerializer()
    currency = AddCurrencySerializer()
    class Meta:
        model = transaction_ibmethod_mdl
        fields = '__all__'


class UpdatecampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterUserCampaign
        fields = '__all__'

class RegisterUserCampaignModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterUserCampaign
        fields = '__all__'
