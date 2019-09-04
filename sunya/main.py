import datetime

from django.shortcuts import render
from django.views import View
from rest_framework import generics, status

# Create your views here.
from rest_framework.response import Response

from account.models import User
from account.salting_hashing import get_salt, hash_string
from sunya.models import Health, Vital_sign, Blood_test, Urine_test
from sunya.serializers import HealthSerializer, UserSerializer, VitalSignSerializer, BloodTestSerializer, UrineTestSerializer


class MainPage(View):
    def get(self, request):
        return render(request, 'health/index.html')


class HealthList(generics.ListCreateAPIView):
    queryset = Health.objects.order_by('user_id', '-created_at').distinct('user_id')
    serializer_class = HealthSerializer

    def create(self, request, *args, **kwargs):
        vital_sign = blood_test = urine_test = None

        username = request.data['user']['username']
        user = User.objects.filter(username=username)
        if user:
            user = user.get()
        else:
            user_details = request.data.pop('user')
            user_serializer = UserSerializer(data=user_details)
            if user_serializer.is_valid():
                user_password = user_details.pop('password')
                salt = get_salt()
                hashed_password = hash_string(salt, user_password)

                user = User(salt=salt, hashed_password=hashed_password, **user_details)
                user.save()
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if 'vital_sign' in request.data:
            vital_sign_serializer = VitalSignSerializer(data=request.data.pop('vital_sign'))
            if vital_sign_serializer.is_valid():
                vital_sign = Vital_sign(user=user, **vital_sign_serializer.data)
                vital_sign.save()
            else:
                return Response(vital_sign_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if 'blood_test' in request.data:
            blood_test_serializer = BloodTestSerializer(data=request.data.pop('blood_test'))
            if blood_test_serializer.is_valid():
                blood_test = Blood_test(user=user, **blood_test_serializer.data)
                blood_test.save()
            else:
                return Response(blood_test_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if 'urine_test' in request.data:
            urine_test_serializer = UrineTestSerializer(data=request.data.pop('urine_test'))
            if urine_test_serializer.is_valid():
                urine_test = Urine_test(user=user, **urine_test_serializer.data)
                urine_test.save()
            else:
                return Response(urine_test_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        created_at = datetime.datetime.now()
        device_id = request.data['device_id']

        health = Health.objects.create(user=user, vital_sign=vital_sign, blood_test=blood_test, urine_test=urine_test,
                                       created_at=created_at, device_id=device_id)
        health.save()

        return Response({"status": "Successfully updated health records!!!"}, status=status.HTTP_201_CREATED)


class HealthDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Health.objects.all()
    serializer_class = HealthSerializer

