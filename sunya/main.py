from django.http import HttpResponse
from django.shortcuts import redirect, render
# Create your views here.

from django.views import View
from django.views.decorators.csrf import csrf_exempt


class MainPage(View):
    def get(self, request):
        return render(request, 'health/index.html')


# @csrf_exempt
def add(request):
    print(request.POST)
    print(request.POST.get('user'))
    return HttpResponse("status: ok")