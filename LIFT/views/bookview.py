import os

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
import requests
from LIFTMAIN.settings import ONEMAP_TOKEN, ONEMAP_DEV_URL

# onemapdev_url = "https://developers.onemap.sg"
# Create your views here.
# @login_required(login_url='/login')
def book(request):

    return render(request, 'book.html')


    # return HttpResponse(data['results'][0]['LONGITUDE'])

def entryLocation(location):
    urls = ONEMAP_DEV_URL+ "/commonapi/search"
    params ={}
    params["searchVal"] = location
    params["returnGeom"] = "Y"
    params["getAddrDetails"] = "Y"
    response = requests.get(urls, params=params)
    return response.json()

def distanceCalculation(startLocation,endLocation):
    urls = ONEMAP_DEV_URL+ "/privateapi/routingsvc/route"
    params ={}
    params["start"] = startLocation
    params["end"] = endLocation
    params["routeType"] = "drive"
    params['token'] = ONEMAP_TOKEN
    response = requests.get(urls, params=params)
    return response.json()

