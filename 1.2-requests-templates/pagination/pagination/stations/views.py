from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
import csv

from pagination.pagination.settings import BUS_STATION_CSV


def index(request):
    return redirect(reverse('bus_stations'))


def read_content():
    result = []
    with open(BUS_STATION_CSV, newline='', encoding='UTF-8') as f:
        reader = csv.DictReader(f)
        for i in reader:
            result.append(i)
    return result


res = read_content()


def bus_stations(request):
    page_number = int(request.GET.get("page", 1))
    paginator = Paginator(res, 10)
    page = paginator.get_page(page_number)
    context = {
        'bus_stations': page.object_list,
        'page': page,
    }
    return render(request, 'stations/index.html', context)