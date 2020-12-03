import csv

from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse


def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    with open(settings.BUS_STATION_CSV, 'r', encoding='cp1251') as file:
        reader = csv.DictReader(file)
        bus_station_list = []
        for row in reader:
            bus_station_list.append(dict(row))

    paginator = Paginator(bus_station_list, 10)
    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    articles = paginator.get_page(current_page)
    data_stations = articles.object_list

    main_url = reverse('bus_stations')
    previous_page, next_page = None, None

    if articles.has_next():
        next_page = main_url + f'?page={articles.next_page_number()}'
    if articles.has_previous():
        previous_page = main_url + f'?page={articles.previous_page_number()}'

    return render(request, 'index.html', context={
        'bus_stations': data_stations,
        'current_page': articles.number,
        'prev_page_url': previous_page,
        'next_page_url': next_page,
    })
