import datetime

from django.db.models import Count, Q

from LIFT.codes import BookingFunctions
from LIFT.codes.BookingFunctions import *
from LIFT.codes.Pathfinder import PathFinder
from LIFT.codes.RiderRequest import riderRequest
from LIFT.codes.Routes import find_nearest
from LIFT.models import models
from LIFT.models.models import PointInfo

search_result = None


def getPrice(request):
    start = request.POST['starting']
    end = request.POST['ending']

    startLoc = PointInfo.objects.get(id=start)
    endLoc = PointInfo.objects.get(id=end)
    totalDistance = BookingFunctions.haversine(startLoc.long, startLoc.lat, endLoc.long,
                                               endLoc.lat)
    print("updated", totalDistance)
    priceDistance = totalDistance

    # Price calculation
    price = 3  # standard price for less than 1km
    priceDistance = int(priceDistance)
    if priceDistance < 3:
        while priceDistance > 0:
            price += 0.22
            priceDistance -= 0.4
    elif priceDistance > 3:
        priceDistance - 10
        price += 0.22 * 0.25
        while priceDistance > 0:
            price += 0.22
            priceDistance -= 0.35
    formatted_price = "{:.2f}".format(price)
    print("The price is: " + str(formatted_price))
    return JsonResponse(formatted_price, safe=False)


def getInfo(request):
    now = 0
    # Selecting type of car/ride
    typeOfRide = request.POST['typeOfRide']
    if str(typeOfRide) == '5 Seater':
        typeOfRide = 5
    elif str(typeOfRide) == '8 Seater':
        typeOfRide = 8
    elif str(typeOfRide) == 'Shared Rides':
        typeOfRide = 1
    print("type of ride", typeOfRide)

    # Current time
    # print(request.POST['pickUpTime'])
    if str(request.POST['pickUpTime']) == 'Now':
        now = datetime.datetime.now()
    # print(now.strftime("%Y %m %d %H %M %S"))

    # User ID
    # print("TEST " + str(request.user.id))  # use this to get user ID

    # Distance
    start = request.POST['starting']
    end = request.POST['ending']

    # print(end)
    startLoc = PointInfo.objects.get(id=start)
    endLoc = PointInfo.objects.get(id=end)
    totalDistance = BookingFunctions.haversine(startLoc.long, startLoc.lat, endLoc.long,
                                               endLoc.lat)
    print("updated", totalDistance)
    priceDistance = totalDistance

    # Price calculation
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
    passengerList = BookingFunctions.createList()
    # User Object
    temp = riderRequest(request.user.id, str(startLoc.lat) + ',' + str(startLoc.long),
                        now.strftime("%Y-%m-%d-%H-%M-%S"), str(endLoc.lat) + ',' + str(endLoc.long), totalDistance,
                        typeOfRide,
                        formatted_price)
    BookingFunctions.addUser(passengerList, temp)
    print("passengerList size", passengerList.size())
    BookingFunctions.findRides(passengerList)

    # BookingFunctions.findRides(passengerList,driverList,standardRideList,sharedList)
    return JsonResponse(formatted_price, safe=False)


def findDriver(request):
    userId = request.user.id
    listStored = findList(int(userId))

    # print("id", userId)
    if int(listStored) == 1:
        print(sharedList.size())
        position = findRideIndex(sharedList, 0, sharedList.size() - 1, userId)
        position = math.ceil(int(position))
        # print("pos", position)
        rideDetail = splitString(str(sharedList.showDetail(int(position))))
        driverId = rideDetail[8]
        # print("driverId", driverId)
        driverName = models.Drivers.objects.get(driverID=driverId).name
        carplate = models.Drivers.objects.get(driverID=driverId).carplate
        # print("drivername carplate", driverName, carplate)
        rideType = "Shared"
        value = [driverId, driverName, carplate, rideType]
        return JsonResponse(value, safe=False)


    elif int(listStored) == 2:
        print(standardRideList.size())
        position = findRideIndex(standardRideList, 0, standardRideList.size() - 1, userId)
        position = math.ceil(int(position))
        rideDetail = splitString(str(standardRideList.showDetail(int(position))))
        driverId = rideDetail[7]
        # print("driverId", driverId)
        driverName = models.Drivers.objects.get(driverID=driverId).name
        carplate = models.Drivers.objects.get(driverID=driverId).carplate
        # print("drivername carplate", driverName, carplate)
        rideType = "Normal"
        value = [driverId, driverName, carplate, rideType]
        return JsonResponse(value, safe=False)


    elif int(listStored) == 3:
        print(sharedList.size())
        mainId = findMainRider(sharedList, userId)
        # print("main Id", mainId)
        position = findRideIndex(sharedList, 0, sharedList.size() - 1, mainId)
        position = math.ceil(int(position))
        rideDetail = splitString(str(sharedList.showDetail(int(position))))
        driverId = rideDetail[8]
        # print("driverId", driverId)
        driverName = models.Drivers.objects.get(driverID=driverId).name
        carplate = models.Drivers.objects.get(driverID=driverId).carplate
        rideType = "Shared"
        # print("drivername carplate", driverName, carplate)

        value = [driverId, driverName, carplate, rideType]
        return JsonResponse(value, safe=False)


def get_address(request):
    if request.method == "GET":
        # search = request.GET.get('search')
        searchval = request.GET['search']
        payload = []
        global search_result
        search_result = PointInfo.objects.exclude(BUILDINGNAME__isnull=True).exclude(BUILDINGNAME__exact='').annotate(
            BUILDINGNAME_count=Count('BUILDINGNAME')).filter(
            Q(BUILDINGNAME__startswith=searchval) | Q(ROAD__startswith=searchval) | Q(POSTALCODE__startswith=searchval))
        searchload = {}
        for search in search_result:
            if search.BUILDINGNAME not in searchload.values():
                if search.BUILDINGNAME != "" and search.BUILDINGNAME != "null":
                    searchload[search.id] = search.BUILDINGNAME
                if search.BLOCK != "":
                    if search.id not in searchload:
                        searchload[search.id] = "BLOCK " + str(search.BLOCK)
                if search.POSTALCODE != "":
                    if search.id not in searchload:
                        searchload[search.id] = search.POSTALCODE
        return JsonResponse(searchload, safe=False)


def getNearest(request):
    if request.method == "GET":
        result = find_nearest(float(request.GET['lat']), float(request.GET['long'])).to_json(orient='records')
        return JsonResponse({'data': result})


def booking_search(request):
    if request.method == "POST":
        startid = request.POST['starting']
        endid = request.POST['ending']
        pf = PathFinder()
        start = PointInfo.objects.get(id=startid)
        end = PointInfo.objects.get(id=endid)

        pf.find_path(start.lat, start.long, end.lat, end.long)
        geom = pf.generate_geojson('LineString')
        return JsonResponse(geom, safe=False)
