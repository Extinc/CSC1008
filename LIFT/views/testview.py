from decimal import Decimal
from math import sqrt

import pandas as pd
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import requests
import json
import datetime
from LIFT.testing import drivertest
from LIFT.testing.drivertest import riderRequest
from LIFT.testing.drivertest import AcceptedRides
from LIFT.codes import BookingFunctions

from LIFTMAIN.settings import MAPBOX_PUBLIC_KEY, ONEMAP_DEV_URL, ONEMAP_TOKEN
from ..codes.Haversine import haversine
from ..codes.Pathfinder import PathFinder
from ..codes.Routes import roadedge_df, roadnode_df, points_df
from ..datastructure.Graph import Graph
# from ..codes.BookingFunctions import dList, aList, rList, sList,

from ..models.models import PointInfo, PathCache


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


def getNearest(request):
    result = find_nearest(float(request.GET['lat']), float(request.GET['long'])).to_json(orient='records')
    return JsonResponse({'data': result})

def find_nearest(lat, long):
    distance = points_df.apply(lambda row: pd.Series({"distance": haversine(long, lat, row['long'], row['lat'])}), result_type='expand', axis= 1)
    df = pd.concat([points_df, distance], axis=1).sort_values(by='distance', ascending=True)
    df = df[df['POSTALCODE'].str.len() > 0]
    return df.head(5)

# Jquery post Request Handling
def plot_route(request):
    if request.method == 'POST':
        graph = Graph()
        endcoord = [1.4410467, 103.839182]
        startcoord = [1.4180309, 103.8386927]
        pf = PathFinder()
        pf.FindPath(startcoord[0],startcoord[1],endcoord[0], endcoord[1])
        geom = pf.generate_geojson()
        return JsonResponse(geom, safe=False)


def getInfo(request):
    #distanceCalculation("1.4180309,103.8386927","1.4410467,103.839182",request)
    print(request.POST['starting'])
    print(request.POST['ending'])

    #Selecting type of car/ride
    typeOfRide = request.POST['typeOfRide']
    if str(typeOfRide) == '5 Seater':
        typeOfRide =5
    elif str(typeOfRide) == '8 Seater':
        typeOfRide =8
    elif str(typeOfRide) == 'Shared Rides':
        typeOfRide =1
    print(typeOfRide)

    #Current time
    print(request.POST['pickUpTime'])
    if str(request.POST['pickUpTime']) == 'Now':
       now = datetime.datetime.now()
    print(now.strftime("%Y %m %d %H %M %S"))
    
    #User ID
    print("TEST " + str(request.user.id))
    
    #Distance
    start = "1.4180309,103.8386927"
    end = "1.4410467,103.839182"
    print(end)
    totalDistance = BookingFunctions.distanceCalculation(start, end)
    print("updated" , totalDistance)
    priceDistance = totalDistance
    
    #Price calculation
    price = 3  # standard price for less than 1km
    priceDistance = int(priceDistance)
    if priceDistance < 10000:
        while priceDistance > 0:
            price += 0.22
            priceDistance -= 400
    elif priceDistance > 10000:
        priceDistance - 10000
        price += 0.22 * 25
        while priceDistance > 0:
            price += 0.22
            priceDistance -= 350
    formatted_price = "{:.2f}".format(price)
    print("The price is: " + str(formatted_price))
    rList = BookingFunctions.createUserList()
    #User Object
    temp = riderRequest(request.user.id,start,now.strftime("%Y %m %d %H %M %S"),end,totalDistance,typeOfRide,formatted_price)
    BookingFunctions.addUser(rList,temp)
    print(rList.listDetail(0))
    print(temp)
    #BookingFunctions.findRides(rList,dList,aList,sList)
    return JsonResponse(formatted_price, safe=False)


def getPrice(request):
    #distanceCalculation("1.4180309,103.8386927","1.4410467,103.839182",request)
    print(request.POST['starting'])
    print(request.POST['ending'])
    start = "1.4180309,103.8386927"
    end = "1.4410467,103.839182"
    print(end)
    totalDistance = BookingFunctions.distanceCalculation(start, end)
    print("updated" , totalDistance)
    priceDistance = totalDistance
    
    #Price calculation
    price = 3  # standard price for less than 1km
    priceDistance = int(priceDistance)
    if priceDistance < 10000:
        while priceDistance > 0:
            price += 0.22
            priceDistance -= 400
    elif priceDistance > 10000:
        priceDistance - 10000
        price += 0.22 * 25
        while priceDistance > 0:
            price += 0.22
            priceDistance -= 350
    formatted_price = "{:.2f}".format(price)
    print("The price is: " + str(formatted_price))
    return JsonResponse(formatted_price, safe=False)

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
