from rest_framework import serializers
import datetime

from account.salting_hashing import get_salt, hash_string
from sunya.models import *


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'address', 'contact_no', 'age', 'gender']


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
    print("test serializer")
    user = UserSerializer()
    vital_sign = VitalSignSerializer(required=False)
    blood_test = BloodTestSerializer(required=False)
    urine_test = UrineTestSerializer(required=False)
    created_at = serializers.DateTimeField(default=datetime.datetime.now())

    class Meta:
        model = Health
        fields = ['id', 'device_id', 'user', 'vital_sign', 'blood_test', 'urine_test', 'created_at']

    def create(self, validated_data):
        user_details = validated_data.pop('user')
        vital_sign_details = validated_data.pop('vital_sign')
        blood_test_details = validated_data.pop('blood_test')
        urine_test_details = validated_data.pop('urine_test')
        created_at = validated_data.pop('created_at')
        device_id = validated_data.pop('device_id')

        # creating a hashed password
        user_password = user_details.pop('password')
        salt = get_salt()
        hashed_password = hash_string(salt, user_password)

        print("\n*********************Test***********************\n")

        user = User(salt=salt, hashed_password=hashed_password, **user_details)
        user.save()

        vital_sign = Vital_sign(user=user, **vital_sign_details)
        blood_test = Blood_test(user=user, **blood_test_details)
        urine_test = Urine_test(user=user, **urine_test_details)

        vital_sign.save()
        blood_test.save()
        urine_test.save()

        health = Health.objects.create(user=user, vital_sign=vital_sign, blood_test=blood_test, urine_test=urine_test,
                                       created_at=created_at, device_id=device_id)

        return health
