import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
import requests
from LIFTMAIN.settings import ONEMAP_TOKEN, MAPBOX_PUBLIC_KEY


onemapdev_url = "https://developers.onemap.sg"
# Create your views here.
def landing_page(request):
    return render(request, 'landing.html')


@login_required(login_url='/login')
def index(request):
    args = {}
    args['title'] = "Home"
    if request.user.is_authenticated:
        args['mapbox_key'] = MAPBOX_PUBLIC_KEY
        fname = request.user.first_name
        args['fname'] = fname
        return render(request, 'index.html', args)
    else:
        return render(request, 'index.html', args)
    # return HttpResponse(data['results'][0]['LONGITUDE'])