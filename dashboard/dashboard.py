from django.shortcuts import render, redirect
from . import context_processors
from account.models import User
# Create your views here.

from django.views import View


class Dashboard(View):
    def get(self, request):

        if 'user' in request.session:
            is_superuser = User.objects.values_list("is_superuser").filter(id=int(request.session['user']))[0][0]
            print("is superuser: %s" % is_superuser)
            context = context_processors.base_variables_all(request)
            return render(request, 'dashboard.html', context)
        else:
            return redirect('login')
