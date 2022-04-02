import datetime

from django.http import JsonResponse

from LIFT.codes import BookingFunctions
from LIFT.codes.RiderRequest import riderRequest
from LIFT.models.models import PointInfo


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
    if priceDistance < 10:
        while priceDistance > 0:
            price += 0.22
            priceDistance -= 0.4
    elif priceDistance > 10:
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
    rList = BookingFunctions.createUserList()
    # User Object
    temp = riderRequest(request.user.id, str(startLoc.lat)+','+str(startLoc.long), now.strftime("%Y-%m-%d-%H-%M-%S"), end, totalDistance, typeOfRide,
                        formatted_price)
    BookingFunctions.addUser(rList, temp)
    print("rList size", rList.size())
    BookingFunctions.findRides(rList)

    # BookingFunctions.findRides(rList,dList,aList,sList)
    return JsonResponse(formatted_price, safe=False)
