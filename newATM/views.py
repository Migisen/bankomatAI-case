from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import View
from django.core import serializers
from .ml import predict_model

from .services import get_atms
from .models import Atm

working_atms = get_atms()


def home(request):
    return render(request, 'home/base.html', {'route': 'home'})


def about(request):
    return render(request, 'about/about.html', {'title': 'О проекте', 'route': 'about'})


def tool(request):
    return render(request, 'tool/tool.html', {'title': 'Инструмент', 'route': 'tool'})


class FeedAjax(View):
    def get(self, request):
        key = 'AIzaSyA6OIckVeIG_7_3DNy1m_tqKqYtzijTws0'
        text = request.GET.get('utility_input')
        print(text)
        if request.is_ajax():
            coordinates = text.split(',')
            print(coordinates)
            result = predict_model.run_prediction(coordinates[0], coordinates[1], key)
            print(result)
            return JsonResponse({'result': result}, status=200)
        return render(request, 'feed/feed.html', {'title': 'Советник', 'route': 'feed'})


class AjaxDashboard(View):
    def get(self, request):
        atm_id = request.GET.get('atm_id')
        atms = Atm.objects.all()
        if request.is_ajax():
            atm = serializers.serialize("json", Atm.objects.filter(id=atm_id))
            return JsonResponse({'atm': atm}, status=200)

        return render(request, 'dashboard/dashboard.html',
                      {'working_atms': atms, 'title': 'Дашборд', 'route': 'dashboard'})
