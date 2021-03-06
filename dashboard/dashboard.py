import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from account.models import User
from sunya.models import Health, Organization_user, Clients, Vital_sign, Blood_test, Urine_test, Organization
from . import context_processors


# Create your views here.


class Dashboard(View):
    def get(self, request):

        if 'user' in request.session:
            user_id = int(request.session['user'])
            is_superuser = User.objects.get(id=user_id).is_superuser
            is_orguser = User.objects.get(id=user_id).is_orguser

            context = context_processors.base_variables_all(request)

            if not is_superuser and is_orguser:
                device_id = Organization_user.objects.filter(user=user_id).get().device_id

                health_list = get_health_list(device_id)
                total_user = Clients.objects.filter(device_id=device_id).count()
                total_tests = Health.objects.filter(device_id=device_id).count()

                context['health_data'] = health_list
                context['total_user'] = total_user
                context['total_tests'] = total_tests

                return render(request, 'health/dashboard_org.html', context)

            org_user_details = get_organization_user_details()
            context['org_user'] = org_user_details

            return render(request, 'health/dashboard.html', context)
        else:
            return redirect('main')


def get_health_list(device_id):
    user = Clients.objects.filter(device_id=device_id)

    if user:
        health_data = list(Health.objects.filter(device=device_id).order_by('user_id', '-created_at')\
            .distinct('user_id').values())

        final_data = []
        for data in health_data:
            dict = {}
            dict['user'] = Clients.objects.filter(user_id=data['user_id']).values()[0]
            dict['vital_sign'] = Vital_sign.objects.filter(id=data['vital_sign_id']).values()[0]
            dict['blood_test'] = Blood_test.objects.filter(id=data['blood_test_id']).values()[0]
            dict['urine_test'] = Urine_test.objects.filter(id=data['urine_test_id']).values()[0]
            final_data.append(dict)

        return final_data
    else:
        return None


def get_health_details(request, user_id):
    try:
        health_id = Health.objects.filter(user=user_id).order_by('-created_at').values('id')
        health_data_list = []
        for h in health_id:
            request_url = request.build_absolute_uri(reverse('health_get', args=(int(h['id']), )))
            health_data = requests.get(request_url).json()
            health_data_list.append(health_data)
        return health_data_list
    except Exception as e:
        print(e)
        return None


def get_organization_user_details():
    organization_user_details = Organization_user.objects.values()
    organization_user_list = []
    for organization_user in organization_user_details:
        device_id = organization_user['device_id']
        user = User.objects.filter(id=organization_user['user_id']).values()[0]
        user['imei'] = Organization.objects.filter(device_id=device_id).get().imei
        user['device_id'] = device_id
        organization_user_list.append(user)

    return organization_user_list

