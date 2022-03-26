from decimal import Decimal

import distance as distance
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import requests
import json
import datetime

from django.utils import timezone

from LIFT.testing import drivertest
from LIFT.testing.drivertest import riderRequest
from LIFT.testing.drivertest import AcceptedRides
from LIFT.codes import BookingFunctions
from math import radians, cos, sin, asin, sqrt
from LIFTMAIN.settings import MAPBOX_PUBLIC_KEY, ONEMAP_DEV_URL, ONEMAP_TOKEN
from ..codes.Routes import roadedge_df, roadnode_df, points_df
from ..datastructure.Graph import Graph, dijkstra
from ..codes.BookingFunctions import dList,aList,rList,sList
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


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km

# Jquery post Request Handling
def plot_route(request):
    if request.method == 'POST':
        graph = Graph()
        endcoord = [1.4410467, 103.839182]
        startcoord = [1.4180309, 103.8386927]
        end = roadnode_df.loc[(roadnode_df['x'] == endcoord[1]) & (roadnode_df['y'] == endcoord[0])]['id'].values[0]
        start = roadnode_df.loc[(roadnode_df['x'] == startcoord[1]) & (roadnode_df['y'] == startcoord[0])]['id'].values[
            0]

        if PathCache.objects.filter(Q(source=start) | Q(destination=end)).count() > 0:
            path_cache = PathCache.objects.get(source=start, destination=end)
            graph.data = json.loads(path_cache.Data)
        else:
            next_node = []
            nodecounter = 0
            graph.addNode(start)

            filtered = roadedge_df.loc[roadedge_df['source'] == start].values
            for node in filtered:
                graph.addEdge(start, node[1], float(node[2]))
                next_node.append(node[1])

            while end not in next_node:
                filtered = roadedge_df.loc[roadedge_df['source'] == next_node[nodecounter]].values
                for next in filtered:
                    if next[1] not in next_node:
                        graph.addEdge(next[0], next[1], float(next[2]))
                        next_node.append(next[1])
                nodecounter += 1
            graph_cache = PathCache.objects.create(source=start,destination=end, DateTime = timezone.now(), Data = json.dumps(graph.data))
            graph_cache.save()

        shortest_path = dijkstra(graph.data, start, end)

        geom = {'type': 'LineString', 'coordinates': []}

        for i in range(len(shortest_path) - 1):
            geom['coordinates'] = geom['coordinates'] + roadedge_df.loc[
                (roadedge_df['source'] == shortest_path[i]) & (roadedge_df['dest'] == shortest_path[i + 1])][
                'geometry'].values[0]
            # print(geom['coordinates'])
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
