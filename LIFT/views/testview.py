import datetime
import json

import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from LIFT.codes import BookingFunctions
from LIFT.codes.RiderRequest import riderRequest
from LIFTMAIN.settings import MAPBOX_PUBLIC_KEY
from ..codes.Pathfinder import PathFinder
from ..codes.Routes import roadedge_df
from ..datastructure.Graph import Graph
from ..models.models import PointInfo


# from ..codes.BookingFunctions import dList, aList, rList, sList,


@login_required(login_url='/login')
def testpage(request):
    args = {'title': "Home"}
    if request.user.is_authenticated:
        print(roadedge_df)
        args['mapbox_key'] = MAPBOX_PUBLIC_KEY
        fname = request.user.first_name
        args['fname'] = fname
        args['pointlist'] = PointInfo.objects.all()
        print(args['pointlist'])
        return render(request, 'test.html', args)
    else:
        return render(request, 'test.html', args)




# get lon n lat of user using ip addr
def select_pickup(request):
    ip = requests.get('https://api.ipify.org?format=json')
    ip_data = json.loads(ip.text)
    res = requests.get('http://ip-api.com/json/' + ip_data['ip'])
    location_data_one = res.text
    location_data = json.loads(location_data_one)
    print("lat: " + str(location_data["lat"]))
    print("lon: " + str(location_data["lon"]))
    return render(request, 'index.html', {'location_data': location_data})

# def distanceCalculation(startLocation, endLocation):
#     urls = ONEMAP_DEV_URL+ "/privateapi/routingsvc/route"
#     params ={}
#     params["start"] = str(startLocation)
#     params["end"] = str(endLocation)
#     params["routeType"] = "drive"
#     params['token'] = ONEMAP_TOKEN
#     response = requests.get(urls, params=params)
#     #print(response.json()["route_summary"]["total_distance"])
#     totaldistance = response.json()["route_summary"]["total_distance"]
#     print("totaldistance is : " + str(totaldistance))
#     return totaldistance
