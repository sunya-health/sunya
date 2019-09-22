import datetime

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from rest_framework import generics, status
# Create your views here.
from rest_framework.response import Response

from account.models import User
from account.salting_hashing import get_salt, hash_string
from dashboard import context_processors
from dashboard.dashboard import get_health_details
from sunya.models import Health, Vital_sign, Blood_test, Urine_test, Organization, Organization_user, Clients
from sunya.serializers import HealthSerializer, VitalSignSerializer, BloodTestSerializer, \
    UrineTestSerializer, ClientSerializer


class MainPage(View):
    def get(self, request):
        return render(request, 'health/index.html')


class ClientReports(View):
    def get(self, request):
        return render(request, 'health/health_report.html')

    def post(self, request):
        user_id = request.POST.get('userID')
        dob = request.POST.get('dob')
        print("user_id: " + user_id)
        print("dob: " + dob)

        client_exists = Clients.objects.filter(user_id=user_id).exists()
        if not client_exists:
            return render(request, "health/index.html",
                          {'error': 1, 'error_message': 'Client does not exist!!!'})

        health_data = get_health_details(request, user_id)
        return render(request, 'health/health_report.html', {'health_details': health_data})


class OrganizationDetails(View):
    def get(self, request):
        if 'user' not in request.session:
            return redirect('main')
        context = context_processors.base_variables_all(request)
        organizations = list(Organization.objects.values())
        context['organization'] = organizations
        context['users'] = list(User.objects.filter(is_orguser=True).values('id', 'username'))
        return render(request, "organization/organization.html", context)

    def post(self, request):
        if request.method == 'POST':
            device_id = request.POST.get('device_id')
            name = request.POST.get('name')
            address = request.POST.get('address')

            Organization.objects.create(device_id=device_id, name=name, address=address)

            return redirect('organization')


def create_user(username, password, f_name, l_name, email, address, contact, age, gender):
    salt = get_salt()
    hashed_password = hash_string(salt, password)
    user = User(username=username, first_name=f_name, last_name=l_name, email=email,
                salt=salt, hashed_password=hashed_password, address=address, contact_no=contact,
                age=age, gender=gender, is_superuser=False, is_orguser=True)

    user.save()

    return user


class AssignOrCreateUser(View):
    def post(self, request):
        if request.method == 'POST':
            device_id = request.POST.get('device_id')
            users = request.POST.get('users')
            username = request.POST.get('username')
            password = request.POST.get('password')
            f_name = request.POST.get('f_name')
            l_name = request.POST.get('l_name')
            email = request.POST.get('email')
            address = request.POST.get('address')
            contact = request.POST.get('contact')
            age = request.POST.get('age')
            gender = request.POST.get('gender')

            device_exists = Organization_user.objects.filter(device=device_id).exists()

            if not device_exists:
                device = Organization.objects.get(device_id=device_id)

                if users == 'None':
                    user_exists = User.objects.filter(username=username).exists()
                    if user_exists:
                        messages.error(request, 'User: %s already exists!!!' % username)
                    else:
                        user = create_user(username, password, f_name, l_name, email, address, contact, age, gender)
                        Organization_user.objects.create(user=user, device=device)
                        messages.success(request, 'Successfully Assigned User!!!')
                else:
                    user = User.objects.get(id=users)
                    Organization_user.objects.create(user=user, device=device)
                    messages.success(request, 'Successfully Assigned User!!!')
            else:
                user_id = Organization_user.objects.get(device=device_id).user_id
                assigned_user = User.objects.get(id=user_id).username
                messages.error(request, 'User is already assigned to a user: %s' % assigned_user)

            return redirect('organization')


class HealthList(generics.ListCreateAPIView):
    queryset = Health.objects.order_by('user_id', '-created_at').distinct('user_id')
    serializer_class = HealthSerializer

    def create(self, request, *args, **kwargs):
        vital_sign = blood_test = urine_test = None

        device_id = request.data['user']['device']
        user_id = request.data['user']['user_id']

        clients = Clients.objects.filter(user_id=user_id)
        device = Organization.objects.filter(device_id=device_id)

        if not device:
            error =  {
                "device": [
                    "Object with device_id=%s does not exist." % device_id
                ]
            }
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        if clients:
            client = clients.get()
            device = device.get()
        else:
            client_details = request.data.pop('user')
            client_serializer = ClientSerializer(data=client_details)

            if client_serializer.is_valid():
                device = Organization.objects.get(device_id=client_details.pop('device'))
                client = Clients(device=device, **client_details)
                client.save()
            else:
                return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if 'vital_sign' in request.data:
            vital_sign_serializer = VitalSignSerializer(data=request.data.pop('vital_sign'))
            if vital_sign_serializer.is_valid():
                vital_sign = Vital_sign(user=client, **vital_sign_serializer.data)
                vital_sign.save()
            else:
                return Response(vital_sign_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if 'blood_test' in request.data:
            blood_test_serializer = BloodTestSerializer(data=request.data.pop('blood_test'))
            if blood_test_serializer.is_valid():
                blood_test = Blood_test(user=client, **blood_test_serializer.data)
                blood_test.save()
            else:
                return Response(blood_test_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if 'urine_test' in request.data:
            urine_test_serializer = UrineTestSerializer(data=request.data.pop('urine_test'))
            if urine_test_serializer.is_valid():
                urine_test = Urine_test(user=client, **urine_test_serializer.data)
                urine_test.save()
            else:
                return Response(urine_test_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        created_at = datetime.datetime.now()

        health = Health.objects.create(user=client, device=device, vital_sign=vital_sign, blood_test=blood_test, urine_test=urine_test,
                                       created_at=created_at)
        health.save()

        return Response({"status": "Successfully updated health records!!!"}, status=status.HTTP_201_CREATED)


class HealthDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Health.objects.all()
    serializer_class = HealthSerializer

