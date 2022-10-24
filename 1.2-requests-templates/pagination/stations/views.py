import csv
from email.policy import default

from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.conf import settings


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    # получите текущую страницу и передайте ее в контекст
    # также передайте в контекст список станций на странице
    with open(settings.BUS_STATION_CSV, 'r', encoding='utf-8') as csvfile:
        data = [item for item in csv.DictReader(csvfile)]
    str_page = request.GET.get('page', default='1')
    if str_page.isnumeric():
        int_page = int(str_page)
    else:
        int_page = 1
    pagi = Paginator(data, 10)
    page = pagi.page(int_page)
    bus_stations = page.object_list

    context = {
        'bus_stations': bus_stations,
        'page': page,
    }
    return render(request, 'stations/index.html', context)
