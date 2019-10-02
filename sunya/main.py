import datetime

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from rest_framework import generics, status
# Create your views here.
from rest_framework.decorators import api_view
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

        client_exists = Clients.objects.filter(user_id=user_id, dob=dob).exists()
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
        organizations_list = []
        for org in organizations:
            values = org.values()
            if 'f' in values or 0 in values:
                org['status'] = 'btn btn-danger'
            elif org['urine_strip'] <= 100 or org['blood_strip'] <= 100:
                org['status'] = 'btn btn-warning'
            else:
                org['status'] = 'btn btn-success'

            device_id = org['device_id']
            org_user = Organization_user.objects.filter(device_id=device_id)
            if org_user:
                user = list(User.objects.filter(id=int(org_user.get().user_id))
                            .values('id', 'username', 'first_name', 'last_name', 'email', 'address', 'contact_no'))[0]
                org['users'] = user
            else:
                org['users'] = {}

            organizations_list.append(org)

        context['organization'] = organizations
        return render(request, "organization/organization.html", context)

    def post(self, request):
        if request.method == 'POST':
            imei = request.POST.get('imei')
            device_id = request.POST.get('device_id')
            name = request.POST.get('name')
            address = request.POST.get('address')
            blood_strip = request.POST.get('blood_strip')
            urine_strip = request.POST.get('urine_strip')

            if Organization.objects.filter(imei=imei).exists():
                messages.error(request, "IMEI: %s already registered." % imei)
            elif Organization.objects.filter(device_id=device_id):
                messages.error(request, "Device ID: %s already registered" % device_id)

            Organization.objects.create(imei=imei, device_id=device_id, name=name, address=address, blood_strip=blood_strip,
                                        urine_strip=urine_strip)

            return redirect('organization')


def create_user(username, password, f_name, l_name, email, address, contact):
    salt = get_salt()
    hashed_password = hash_string(salt, password)
    user = User(username=username, first_name=f_name, last_name=l_name, email=email,
                salt=salt, hashed_password=hashed_password, address=address, contact_no=contact, is_superuser=False, is_orguser=True)

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

            device_exists = Organization_user.objects.filter(device=device_id).exists()

            if not device_exists:
                device = Organization.objects.get(device_id=device_id)

                if users is None:
                    user_exists = User.objects.filter(username=username).exists()
                    if user_exists:
                        messages.error(request, 'User: %s already exists!!!' % username)
                    else:
                        user = create_user(username, password, f_name, l_name, email, address, contact)
                        Organization_user.objects.create(user=user, device=device)
                        messages.success(request, 'Successfully Assigned User!!!')
                else:
                    user = User.objects.get(id=users)
                    Organization_user.objects.create(user=user, device=device)
                    messages.success(request, 'Successfully Assigned User!!!')
            else:
                device = Organization.objects.get(device_id=device_id)
                user_id = Organization_user.objects.get(device=device_id).user_id
                assigned_user = User.objects.get(id=user_id).username

                if username == assigned_user:
                    messages.error(request, 'User: %s is already assigned to this device!!!' % username)
                else:
                    user = create_user(username, password, f_name, l_name, email, address, contact)
                    Organization_user.objects.filter(device=device).update(user=user)
                    User.objects.get(id=int(user_id)).delete()
                    messages.success(request, 'Successfully Assigned User!!!')

            return redirect('organization')


class StripUpdate(View):
    def post(self, request):
        if request.method == 'POST':
            org_id = int(request.POST.get('org_id'))
            blood_strip = int(request.POST.get('blood_strip'))
            urine_strip = int(request.POST.get('urine_strip'))

            try:
                Organization.objects.filter(id=org_id).update(
                    blood_strip=blood_strip, urine_strip=urine_strip)
            except Exception as e:
                print(e)

            return redirect('organization')


class HealthList(generics.ListCreateAPIView):
    queryset = Health.objects.order_by('user_id', '-created_at').distinct('user_id')
    serializer_class = HealthSerializer

    def create(self, request, *args, **kwargs):
        try:
            for data in request.data:
                vital_sign = blood_test = urine_test = None

                device_id = data['user']['device']
                user_id = data['user']['user_id']

                clients = Clients.objects.filter(user_id=user_id)
                device = Organization.objects.filter(device_id=device_id)

                if not device:
                    return Response({"status": 0, "msg": "Object with device_id=%s does not exist." % device_id}, status=status.HTTP_400_BAD_REQUEST)

                blood_strip = device.get().blood_strip
                urine_strip = device.get().urine_strip

                if blood_strip == 0 and urine_strip == 0:
                    return Response({"status": 0, "msg": "Blood strip and Urine strip not available"}, status=status.HTTP_400_BAD_REQUEST)
                elif blood_strip == 0:
                    return Response({"status": 0, "msg": "Blood strip not available"}, status=status.HTTP_400_BAD_REQUEST)
                if urine_strip == 0:
                    return Response({"status": 0, "msg": "Urine strip not available"}, status=status.HTTP_400_BAD_REQUEST)

                blood_strip = blood_strip - 1
                urine_strip = urine_strip - 1

                if clients:
                    client = clients.get()
                    device = device.get()
                else:
                    client_details = data.pop('user')
                    client_serializer = ClientSerializer(data=client_details)

                    if client_serializer.is_valid():
                        device = Organization.objects.get(device_id=client_details.pop('device'))
                        client = Clients(device=device, **client_details)
                        client.save()
                    else:
                        return Response({"status": 0, "msg": client_serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)

                if 'vital_sign' in data:
                    vital_sign_serializer = VitalSignSerializer(data=data.pop('vital_sign'))
                    if vital_sign_serializer.is_valid():

                        v_data = vital_sign_serializer.data

                        temperature_sensor = 't' if 'temperature' in v_data else 'f'
                        weighing_machine = 't' if 'weight' in v_data else 'f'
                        measuring_tool = 't' if 'height' in v_data else 'f'
                        bp_sensor = 't' if 'bp_diastolic' in v_data or 'bp_systoic' in v_data else 'f'
                        pulse_sensor = 't' if 'pulse' in v_data else 'f'

                        Organization.objects.filter(device_id=device_id).update(
                            temperature_sensor=temperature_sensor,
                            weighing_machine=weighing_machine,
                            measuring_tool=measuring_tool,
                            bp_sensor=bp_sensor,
                            pulse_sensor=pulse_sensor
                        )

                        vital_sign = Vital_sign(user=client, **v_data)
                        vital_sign.save()
                    else:
                        return Response({"status": 0, "msg": vital_sign_serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)

                if 'blood_test' in data:
                    blood_test_serializer = BloodTestSerializer(data=data.pop('blood_test'))
                    if blood_test_serializer.is_valid():
                        blood_test = Blood_test(user=client, **blood_test_serializer.data)
                        blood_test.save()

                        blood_sensor = 't'
                    else:
                        return Response({"status": 0, "msg": blood_test_serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    blood_sensor = 'f'

                if 'urine_test' in data:
                    urine_test_serializer = UrineTestSerializer(data=data.pop('urine_test'))
                    if urine_test_serializer.is_valid():
                        urine_test = Urine_test(user=client, **urine_test_serializer.data)
                        urine_test.save()

                        urine_device = 't'
                    else:
                        return Response({"status": 0, "msg": urine_test_serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    urine_device = 'f'

                Organization.objects.filter(device_id=device_id).update(
                    blood_sensor=blood_sensor,
                    urine_device=urine_device,
                    blood_strip=blood_strip,
                    urine_strip=urine_strip
                )

                # created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                created_at = datetime.datetime.now().date()

                health = Health.objects.create(user=client, device=device, vital_sign=vital_sign, blood_test=blood_test, urine_test=urine_test,
                                               created_at=created_at)
                health.save()

            return Response(
                {
                    "status": 1,
                    "msg": "Successfully updated health records!!!"
                }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {
                    "status": 0,
                    "msg": e
                }, status=status.HTTP_201_CREATED)


class HealthDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Health.objects.all()
    serializer_class = HealthSerializer


@api_view(['GET'])
def organization_device_details(request, pk):
    imei_exists = Organization.objects.filter(imei=pk).exists()
    if imei_exists:
        device_id = Organization.objects.filter(imei=pk).get().device_id
        user_id = Clients.objects.filter(device_id=device_id).order_by('-user_id')[:1].get().user_id    # end user
        return Response({"status": 1, "device_id": device_id, "user_id": user_id}, status=status.HTTP_200_OK)
    else:
        return Response({"status": 0}, status=status.HTTP_204_NO_CONTENT)







