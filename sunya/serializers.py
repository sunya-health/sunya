from rest_framework import serializers
import datetime
from sunya.models import *


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'address', 'contact_no', 'age', 'gender']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = ['user_id', 'device', 'first_name', 'last_name', 'email', 'address', 'contact_no', 'age', 'gender']



class VitalSignSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vital_sign
        fields = ['weight', 'height', 'temperature', 'pulse', 'bp_systolic', 'bp_diastolic', 'sto2']


class BloodTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blood_test
        fields = ['glucose', 'cholesterol', 'uric_acid']


class UrineTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Urine_test
        fields = ['leukocytes', 'nitrate', 'urobilinogen', 'protein', 'ph', 'blood', 'sp_gravity', 'ketone', 'bilirubin', 'glucose', 'ascorbic_acid']


class HealthSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    user = ClientSerializer()
    vital_sign = VitalSignSerializer(required=False)
    blood_test = BloodTestSerializer(required=False)
    urine_test = UrineTestSerializer(required=False)
    created_at = serializers.DateTimeField(default=datetime.datetime.now())

    class Meta:
        model = Health
        fields = ['id', 'user', 'vital_sign', 'blood_test', 'urine_test', 'created_at']




