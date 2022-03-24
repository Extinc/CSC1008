from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import requests
import json

from LIFTMAIN.settings import MAPBOX_PUBLIC_KEY, ONEMAP_DEV_URL, ONEMAP_TOKEN
from ..codes.Routes import roadedge_df,roadnode_df
from ..datastructure.Graph import Graph, dijkstra

@login_required(login_url='/login')
def testpage(request):
    args = {'title': "Home"}
    if request.user.is_authenticated:
        print(roadedge_df)
        args['mapbox_key'] = MAPBOX_PUBLIC_KEY
        fname = request.user.first_name
        args['fname'] = fname
        print(request.user.id)
        return render(request, 'test.html', args)
    else:
        return render(request, 'test.html', args)


# Jquery post Request Handling
def plot_route(request):
    if request.method == 'POST':
        graph = Graph()
        endcoord = [1.4410467, 103.839182]
        startcoord = [1.4180309, 103.8386927]
        end = roadnode_df.loc[(roadnode_df['x'] == endcoord[1]) & (roadnode_df['y'] == endcoord[0])]['id'].values[0]
        start = roadnode_df.loc[(roadnode_df['x'] == startcoord[1]) & (roadnode_df['y'] == startcoord[0])]['id'].values[
            0]

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

        shortest_path = dijkstra(graph.data, start, end)

        geom = {'type': 'LineString', 'coordinates': []}

        for i in range(len(shortest_path) - 1):
            geom['coordinates'] = geom['coordinates'] + roadedge_df.loc[
                (roadedge_df['source'] == shortest_path[i]) & (roadedge_df['dest'] == shortest_path[i + 1])][
                'geometry'].values[0]
            # print(geom['coordinates'])
        return JsonResponse(geom, safe=False)


def getInfo(request):
    # distanceCalculation("1.4180309,103.8386927","1.4410467,103.839182",request)
    print(request.POST['starting'])
    print(request.POST['ending'])
    print(request.POST['typeOfRide'])
    print(request.POST['pickUpTime'])
    # start = request.POST['starting'] #same for end
    # print("TEST " + str(request.user.id))
    start = "1.4180309,103.8386927"
    # end = request.POST['ending'] #we can delete the one below once we retrieve the vals
    end = "1.4410467,103.839182"
    print(end)
    totaldistance = distanceCalculation(start, end)
    print(totaldistance)
    # urls = ONEMAP_DEV_URL+ "/privateapi/routingsvc/route"
    # params ={}
    # params["start"] = "1.4180309,103.8386927"
    # params["end"] = "1.4410467,103.839182"
    # params["routeType"] = "drive"
    # params['token'] = ONEMAP_TOKEN
    # response = requests.get(urls, params=params)
    # #print(response.json()["route_summary"]["total_distance"])
    # totaldistance = response.json()["route_summary"]["total_distance"]
    # getPrice(totaldistance,request)
    print("totaldistance is : " + str(totaldistance))

    price = 3  # standard price for less than 1km

    if totaldistance < 10000:
        while totaldistance > 0:
            price += 0.22
            totaldistance -= 400
    elif totaldistance > 10000:
        totaldistance - 10000
        price += 0.22 * 25
        while totaldistance > 0:
            price += 0.22
            totaldistance -= 350
    # if typeOfCar == "8 seater":
    #     price*=1.5
    formatted_price = "{:.2f}".format(price)
    print("The price is: " + str(formatted_price))
    return JsonResponse(formatted_price, safe=False)
    # return HttpResponse(request)


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


def distanceCalculation(startLocation, endLocation):
    urls = ONEMAP_DEV_URL + "/privateapi/routingsvc/route"
    params = {}
    params["start"] = "1.4410467,103.839182"
    params["end"] = "1.4410467,103.839182"
    params["routeType"] = "drive"
    params['token'] = ONEMAP_TOKEN
    response = requests.get(urls, params=params)
    return response.json()
