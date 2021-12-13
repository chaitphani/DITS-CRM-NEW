from rest_framework import serializers
from sportapp.models import Register, RegisterUserCampaign

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        #fields = ['id', 'client_id']
        fields='__all__'


class RegisterUserCampaignSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterUserCampaign
        fields = ['object_status', 'ref_code', 'campaign_code', 'campaign']