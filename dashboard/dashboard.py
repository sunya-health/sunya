import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from account.models import User
from sunya.models import Health
from . import context_processors


# Create your views here.


class Dashboard(View):
    def get(self, request):

        if 'user' in request.session:
            user_id = int(request.session['user'])
            is_superuser = User.objects.get(id=user_id).is_superuser
            context = context_processors.base_variables_all(request)

            if not is_superuser:
                health_data = get_health_details(request, user_id)
                context['health_details'] = health_data
                return render(request, 'dashboard_user.html', context)

            health_list = get_health_list(request)
            print(health_list)
            context['health_data'] = health_list
            return render(request, 'dashboard.html', context)
        else:
            return redirect('main')


def get_health_list(request):
    request_url = request.build_absolute_uri(reverse('health_add'))
    health_data = requests.get(request_url).json()
    health_list = []

    for data in health_data:
        user_details = data['user']
        vital_sign_details = data['vital_sign']
        blood_test_details = data['blood_test']
        urine_test_details = data['urine_test']

        # show_details = "<button type=\"button\" id=\""+user_details['username']+"\" data-toggle=\"modal\" data-target=\"#healthModal\" " \
        #                                                                         "class=\"btn btn-action\" data-values='{" \
        #                                                         "\"user\": "+user_details+"" \
        #                                                         "\"vital_sign\": "+vital_sign_details+"" \
        #                                                         "\"blood_test\": "+blood_test_details+"" \
        #                                                         "\"urine_test\": "+urine_test_details+"" \
        #                                                         "}'>details</button>"

        show_details = "<button type=\"button\" data-toggle=\"modal\" data-target=\"#healthModal\" " \
                                                                                    "class=\"btn btn-action\" data-values='{" \
                                                                                    "\"user\": \"test_user\"}'>details</button>"



        health_list.append([user_details['username'], user_details['first_name'], user_details['last_name'], user_details['address'],
                            user_details['contact_no'], user_details['email'], user_details['age'], user_details['gender'], show_details])
    return health_list


def get_health_details(request, user_id):
    try:
        health_id = int(Health.objects.get(user=user_id).id)
        request_url = request.build_absolute_uri(reverse('health_get', args=(health_id, )))

        health_data = requests.get(request_url).json()
        return health_data
    except Exception:
        return None
