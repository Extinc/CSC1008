import math

from django.http import JsonResponse
from LIFT.codes.AcceptedRides import AcceptedRides
from LIFT.codes.Driver import Driver
from LIFT.codes.RiderRequest import riderRequest
from LIFT.codes.SharedRides import SharedRides
from LIFT.datastructure.HashTable import HashTable
from LIFT.datastructure.linkedList import SinglyLinkedList
from LIFTMAIN.settings import ONEMAP_DEV_URL, ONEMAP_TOKEN
from math import radians, cos, sin, asin, sqrt
import requests
from LIFT.models import models


def createUserList():
    userList = SinglyLinkedList()
    return userList


def addUser(userList, object):
    userList.insertAtEnd(object)


def splitString(userString):
    return str(userString).split(' ')


def splitByComma(userString):
    return str(userString).split(',')


def findNearestRider(rList, sList, driver):
    firstRider = splitString(str(rList.listDetail(0)))
    # print("TEST EEFCODE 1 :  ",rList.listDetail(0))
    for i in range(1, rList.size() - 1):
        location = str(dList[i].driverlat) + "," + str(dList[i].driverlong)
        nextRider = splitString(str(rList.listDetail(int(i))))
        firstRiderLoc = splitByComma(str(firstRider[1]))
        nextRiderLoc = splitByComma(str(nextRider[1]))
        firstRiderDest = splitByComma(str(firstRider[3]))
        # print("TEST EEFCODE 1 :  ",float(nextRiderLoc[0]))
        print("TEST EEFCODE 1 first rider dest :  ", firstRiderDest)
        print("TEST EEFCODE 1 next rider dest :  ", nextRiderLoc)
        pToP = haversine(float(firstRiderLoc[1]), float(firstRiderLoc[0]), float(nextRiderLoc[1]),
                         float(nextRiderLoc[0]))  # compare pickup for rider 1 and next rider
        #
        pToD = haversine(float(firstRiderDest[1]), float(firstRiderDest[0]), float(nextRiderLoc[1]),
                         float(nextRiderLoc[0]))  # compare dropoff for rider 1 and pickup for rider2
        if (int(pToP) < 5 or int(pToD) < 5 and int(nextRider[5]) == 1):  # check if in range
            if pToP >= pToD:
                newSR = SharedRides(firstRider[0], nextRider[0], firstRider[1], firstRider[3], nextRider[1],
                                    nextRider[3], location, firstRider[2], firstRider[5],
                                    driver.driverID)  # for when its destination is closer to first rider so car goes from
                addUser(sList, newSR)
                uTable.setVal(firstRider[0],
                              "1")  # sharedRide = 1, AcceptedRides = 2. We just need to store an ID for one user since its a shared ride
                print("New Shared Ride", sList.size())
            else:
                newSR = SharedRides(firstRider[0], nextRider[0], firstRider[1], nextRider[1], firstRider[3],
                                    nextRider[3], location, firstRider[2], firstRider[5],
                                    driver.driverID)  # normal case where it picks up passenger along the way

                addUser(sList, newSR)
                sortSList(sList)
                uTable.setVal(firstRider[0], "1")
                uTable.setVal(nextRider[0], "3")

            print("New Shared Ride", sList.listDetail(int(sList.size() - 2)))
            rList.deleteAt(i)
            return True

        return False


def findMainRider(list, userId):  # uses binary search
    # def binarySearch(arr, l, r, x): #l = first value r = last val x = value we searching
    for i in range(list.size()):
        rideDetail = splitString(str(list.listDetail(int(i))))
        if rideDetail[1] == userId:
            return rideDetail[0]


def findRides(rList):  # aList =Accepted Rides sList= Shared Rides rList = ridersList
    addUser(rList, Rider2)  # add dummy rider
    print("rider Detail", rList.listDetail(int(0)))
    rider = splitString(str(rList.listDetail(int(0))))  # retrieve first rider details
    i = 0

    for driver in dList:

        location = str(dList[i].driverlat) + "," + str(dList[i].driverlong)

        riderLoc = splitByComma(str(rider[1]))
        # print(rider[1])
        # print("location",location)
        if haversine(float(str(dList[i].driverlat)), float(str(dList[i].driverlong)), float(riderLoc[0]),
                     float(riderLoc[1])) < 5:
            driverDetails = dList[i]
            print("distance within 5km")
            if int(rider[5]) == 1:
                sharedCheck = findNearestRider(rList, sList, driverDetails)
                if sharedCheck == True:
                    print("Shared Rides")
                    rList.deleteAt(0)
                    break
                else:
                    print("No Shared Ride Found")
                    newRide = AcceptedRides(rider[0], rider[1], location, rider[2], rider[3], rider[4], rider[6],
                                            rider[5], driverDetails.driverID)
                    addUser(aList, newRide)
                    sortAList(aList)
                    uTable.setVal(rider[0], "2")
                    # needa delete but whatevs
                    rList.deleteAt(0)
                    print("aList details,", aList.listDetail(int(0)))
                    break
            elif (int(rider[5]) == int(5)):
                print("5 or 8")
                if int(rider[5]) <= int(dList[i].seatNo):
                    newRide = AcceptedRides(rider[0], rider[1], location, rider[2], rider[3], rider[4], rider[6],
                                            rider[5], driverDetails.driverID)
                    print("new Ride", newRide)
                    addUser(aList, newRide)

                    print(aList.listDetail(0))
                    sortAList(aList)
                    uTable.setVal(rider[0], "2")

                    print("Rider Id")
                    print(rider[0])
                    # needa delete but whatevs
                    rList.deleteAt(0)
                    print("accepted", aList.listDetail(0))
                    break
            elif (int(rider[5]) == int(8)):
                if int(rider[5]) == int(dList[i].seatNo):
                    newRide = AcceptedRides(rider[0], rider[1], location, rider[2], rider[3], rider[4], rider[6],
                                            rider[5], driverDetails.driverID)

                    addUser(aList, newRide)

                    print(aList.listDetail(0))
                    sortAList(aList)
                    print("Rider Id")
                    print(rider[0])
                    uTable.setVal(rider[0], "2")
                    # needa delete but whatevs
                    rList.deleteAt(0)
                    print("accepted", aList.listDetail(0))
                    break
            else:
                print(dList[i].seatNo)
                print("no same seat")
                break

        i += 1


def findList(userId):  # hashmap to delete
    print(uTable)
    listStored = uTable.getVal(str(userId))
    print("List Stored")
    print(str(listStored))
    return listStored


def sortAList(list):
    for m in range(list.size() - 1, 0, -1):
        for n in range(m):

            aRide1 = splitString(str(aList.listDetail(int(n))))
            aRide2 = splitString(str(aList.listDetail(int(n + 1))))
            print("1", aRide1[0])
            print("2", aRide2[0])
            if (aRide2[0] is not None):
                if aRide1[0] > aRide2[0]:
                    temp = AcceptedRides(aRide1[0], aRide1[1], aRide1[2], aRide1[2], aRide1[3], aRide1[4], aRide1[5],
                                         aRide1[6], aRide1[7])

                    aList.deleteAt(n)
                    addUser(aList, temp)

        print("one set")


def sortSList(list):
    for m in range(list.size() - 1, 0, -1):
        for n in range(m):

            sRide1 = splitString(str(sList.listDetail(int(n))))
            sRide2 = splitString(str(sList.listDetail(int(n + 1))))
            print("1", sRide1[0])
            print("2", sRide2[0])
            if (sRide2[0] is not None):
                if sRide1[0] > sRide2[0]:
                    temp = AcceptedRides(sRide1[0], sRide1[1], sRide1[2], sRide1[2], sRide1[3], sRide1[4], sRide1[5],
                                         sRide1[6], sRide1[7], sRide1[8], sRide1[9])

                    aList.deleteAt(n)
                    addUser(aList, temp)

        print("one set")


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
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    km = 6371 * c
    # print(km)
    return km


def distanceCalculation(startLocation, endLocation):
    urls = ONEMAP_DEV_URL + "/privateapi/routingsvc/route"
    params = {}
    params["start"] = str(startLocation)
    params["end"] = str(endLocation)
    params["routeType"] = "drive"
    params['token'] = ONEMAP_TOKEN
    response = requests.get(urls, params=params)
    # print(response.json()["route_summary"]["total_distance"])
    totaldistance = response.json()["route_summary"]["total_distance"]
    print("totaldistance is : " + str(totaldistance))
    return totaldistance


def findRideIndex(list, smallest, size, userId):  # uses binary search
    # def binarySearch(arr, l, r, x): #l = first value r = last val x = value we searching
    if size > smallest:
        mid = smallest + (size - smallest) / 2
        print(mid)
        print(size)
        print("userId in index", userId)
        currentId = splitString(str(list.listDetail(mid)))
        print(currentId[0])
        if currentId[0] is None or int(mid) >= 0 and int(mid) <= 1:
            return 0

        elif int(currentId[0]) == int(userId):
            return mid

        elif int(currentId[0]) > int(userId):
            return findRideIndex(list, smallest, mid - 1, userId)

        else:

            return findRideIndex(list, mid + 1, size, userId)
    else:
        return 0


def endRide(request):
    userId = request.POST['userId']
    listStored = findList(userId)

    if int(listStored) == 1:
        print(sList.size())
        print("main id", userId)
        position = findRideIndex(sList, 0, sList.size() - 1, userId)
        position = math.ceil(int(position))
        sList.deleteAt(position)
        uTable.delVal(userId)
        ended = "Shared Ride Has Ended"
        return JsonResponse(ended, safe=False)
    elif int(listStored) == 2:
        print(aList.size())
        print("main id", userId)
        position = findRideIndex(aList, 0, aList.size() - 1, userId)
        position = math.ceil(int(position))
        aList.deleteAt(int(position))
        uTable.delVal(userId)
        ended = "Normal Ride Has Ended"
        return JsonResponse(ended, safe=False)
    elif int(listStored) == 3:
        print(sList.size())
        mainId = findMainRider(sList, userId)
        print("main id", mainId)
        position = findRideIndex(sList, 0, sList.size() - 1, mainId)
        position = math.ceil(int(position))
        sList.deleteAt(position)
        uTable.delVal(mainId)
        uTable.delVal(userId)
        ended = "Shared Ride Has Ended"
        return JsonResponse(ended, safe=False)


# creating all the Linked List and functions we will use
dList = models.Drivers.objects.all()
rList = createUserList()
aList = createUserList()
sList = createUserList()
uTable = HashTable()
Rider2 = riderRequest("2103", "1.4240931,103.8390675", "1331522", "1.4410467,103.839182", 31023, 1,
                      '20')

