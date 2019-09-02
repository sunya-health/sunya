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
        fields = '__all__'


class BloodTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blood_test
        fields = '__all__'


class UrinTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Urine_test
        fields = '__all__'


class HealthSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    vital_sign = VitalSignSerializer()
    blood_test = BloodTestSerializer()
    urine_test = UrinTestSerializer()
    created_at = serializers.DateTimeField(default=datetime.datetime.now())

    class Meta:
        model = Health
        fields = ['id', 'user', 'vital_sign', 'blood_test', 'urine_test', 'created_at']

    def create(self, validated_data):
        user_details = validated_data.pop('user')
        vital_sign_details = validated_data.pop('vital_sign')
        blood_test_details = validated_data.pop('blood_test')
        urine_test_details = validated_data.pop('urine_test')
        created_at = validated_data.pop('created_at')

        # creating a hashed password
        user_password = user_details.pop('password')
        salt = get_salt()
        hashed_password = hash_string(salt, user_password)

        user = User(salt=salt, hashed_password=hashed_password, **user_details)
        vital_sign = Vital_sign.objects.create(**vital_sign_details)
        blood_test = Blood_test.objects.create(**blood_test_details)
        urine_test = Urine_test.objects.create(**urine_test_details)

        user.save()
        vital_sign.save()
        blood_test.save()
        urine_test.save()

        health = Health.objects.create(user=user, vital_sign=vital_sign, blood_test=blood_test, urine_test=urine_test, created_at=created_at)

        return health
