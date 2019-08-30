from django.shortcuts import render, redirect
from . import context_processors
from account.models import User
# Create your views here.

from django.views import View


class Dashboard(View):
    def get(self, request):

        if 'user' in request.session:
            user_id = int(request.session['user'])
            is_superuser = User.objects.get(id=user_id).is_superuser
            context = context_processors.base_variables_all(request)

            if not is_superuser:
                # return render(request, 'dashboard_user.html', context)
                return render(request, 'health/index.html', context)

            return render(request, 'dashboard.html', context)
        else:
            return redirect('login')
