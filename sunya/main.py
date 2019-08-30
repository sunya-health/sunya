from django.shortcuts import redirect, render
# Create your views here.

from django.views import View


class MainPage(View):
    def get(self, request):
        return render(request, 'health/index.html')
