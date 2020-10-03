from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
from django.core import serializers

from .data_processing import get_info
from .ml import predict_model
#from .data_processing import get_info

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
    key = 'AIzaSyA6OIckVeIG_7_3DNy1m_tqKqYtzijTws0'
    def get(self, request):
        key = self.key
        unique_cities = Atm.objects.order_by().values('settlement').distinct()
        result = None
        if request.is_ajax():
            text = request.GET.get('utility_input')
            selected = request.GET.get('city')
            if text is not None:
                coordinates = text.split(',')
                print(coordinates)
                result = predict_model.run_prediction(float(coordinates[0]), float(coordinates[1])).predict[0]
                print(result)
                result = round(result, 1)
            if selected is not None:
                requested_cities = Atm.objects.filter(settlement=selected)
                print(get_info(requested_cities, key))

            return JsonResponse({'result': result, 'selected': selected}, status=200)
        return render(request, 'feed/feed.html', {'unique_cities': unique_cities, 'title': 'Советник', 'route': 'feed'})




class AjaxDashboard(View):
    def get(self, request):
        atm_id = request.GET.get('atm_id')
        atms = Atm.objects.all()
        if request.is_ajax():
            atm = serializers.serialize("json", Atm.objects.filter(id=atm_id))
            return JsonResponse({'atm': atm}, status=200)

        return render(request, 'dashboard/dashboard.html',
                      {'working_atms': atms, 'title': 'Дашборд', 'route': 'dashboard'})
