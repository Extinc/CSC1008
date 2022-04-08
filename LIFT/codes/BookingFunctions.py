import math
from math import radians, cos, sin, asin, sqrt

from django.http import JsonResponse

from LIFT.codes.AcceptedRides import AcceptedRides
from LIFT.codes.RiderRequest import riderRequest
from LIFT.codes.SharedRides import SharedRides
from LIFT.datastructure.HashTable import HashTable
from LIFT.datastructure.linkedList import SinglyLinkedList
from LIFT.models import models


def createList():
    list = SinglyLinkedList()
    return list


def addUser(list, object):
    list.insertAtEnd(object)


# Split string by space
def splitString(userString):
    return str(userString).split(' ')


# Split string by comma
def splitByComma(userString):
    return str(userString).split(',')


def findNearestRider(passengerList, sharedList, driver):
    firstRider = splitString(str(passengerList.showDetail(0)))

    for i in range(1, passengerList.size() - 1):
        location = str(driverList[i].driverlat) + "," + str(driverList[i].driverlong)
        nextRider = splitString(str(passengerList.showDetail(int(i))))
        firstRiderLoc = splitByComma(str(firstRider[1]))

        # getting second rider location
        nextRiderLoc = splitByComma(str(nextRider[1]))
        firstRiderDest = splitByComma(str(firstRider[3]))

        # use haversine function to get distance
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
                addUser(sharedList, newSR)
                uTable.setVal(firstRider[0],
                              "1")  # sharedRide = 1, AcceptedRides = 2. We just need to store an ID for one user since its a shared ride
            else:
                newSR = SharedRides(firstRider[0], nextRider[0], firstRider[1], nextRider[1], firstRider[3],
                                    nextRider[3], location, firstRider[2], firstRider[5],
                                    driver.driverID)  # normal case where it picks up passenger along the way

                addUser(sharedList, newSR)
                sortsharedList(sharedList)

                # adds first rider and secondary rider into the hashmap
                uTable.setVal(firstRider[0], "1")
                # shared rides but cannot find another rider, so '3'
                uTable.setVal(nextRider[0], "3")

            passengerList.deleteAt(i)
            return True

        return False


def findMainRider(list, userId):  # uses binary search
    # def binarySearch(arr, l, r, x): #l = first value r = last val x = value we searching
    for i in range(list.size()):
        rideDetail = splitString(str(list.showDetail(int(i))))
        if rideDetail[1] == userId:
            return rideDetail[0]


def findRides(
        passengerList):  # standardRideList =Accepted Rides sharedList= Shared Rides passengerList = ridersharedList
    addUser(passengerList, Rider2)  # add dummy rider
    rider = splitString(str(passengerList.showDetail(int(0))))  # retrieve first rider details

    for driver in driverList:

        location = str(driver.driverlat) + "," + str(driver.driverlong)

        riderLoc = splitByComma(str(rider[1]))

        if haversine(float(str(driver.driverlat)), float(str(driver.driverlong)), float(riderLoc[0]),
                     float(riderLoc[1])) < 2:  # checks if distance is less than 2km
            driverDetails = driver
            # if shared rides is chosen
            if int(rider[5]) == 1:
                sharedCheck = findNearestRider(passengerList, sharedList, driverDetails)
                if sharedCheck:
                    passengerList.deleteAt(0)
                    break
                else:
                    # if shared rides is chosen but no shared rides are found, add to accepted
                    # Putting him in a new ride
                    newRide = AcceptedRides(rider[0], rider[1], location, rider[2], rider[3], rider[4], rider[6],
                                            rider[5], driverDetails.driverID)
                    addUser(standardRideList, newRide)
                    sortstandardRideList(standardRideList)
                    uTable.setVal(rider[0], "2")
                    # needa delete but whatevs
                    passengerList.deleteAt(0)
                    break
            elif (int(rider[5]) == int(5)):
                # add to accepted rides
                if int(rider[5]) <= int(driver.seatNo):
                    newRide = AcceptedRides(rider[0], rider[1], location, rider[2], rider[3], rider[4], rider[6],
                                            rider[5], driverDetails.driverID)
                    addUser(standardRideList, newRide)

                    sortstandardRideList(standardRideList)
                    uTable.setVal(rider[0], "2")
                    # needa delete but whatevs
                    passengerList.deleteAt(0)
                    break
                # if no. of seats = 8
            elif (int(rider[5]) == int(8)):
                # add to accepted rides
                if int(rider[5]) == int(driver.seatNo):
                    newRide = AcceptedRides(rider[0], rider[1], location, rider[2], rider[3], rider[4], rider[6],
                                            rider[5], driverDetails.driverID)

                    addUser(standardRideList, newRide)

                    sortstandardRideList(standardRideList)
                    # setting hashtable to accepted
                    uTable.setVal(rider[0], "2")
                    # needa delete but whatevs
                    passengerList.deleteAt(0)
                    break
            else:
                break

    # find which type of rides the user is in


def findList(userId):  # hashmap to delete
    listStored = uTable.getVal(str(userId))
    return listStored

    # sort Accepted List


def sortstandardRideList(list):
    for m in range(list.size() - 1, 0, -1):
        for n in range(m):

            aRide1 = splitString(str(standardRideList.showDetail(int(n))))
            aRide2 = splitString(str(standardRideList.showDetail(int(n + 1))))
            if (aRide2[0] is not None):
                if aRide1[0] > aRide2[0]:
                    # add new accepted rides entry
                    temp = AcceptedRides(aRide1[0], aRide1[1], aRide1[2], aRide1[2], aRide1[3], aRide1[4], aRide1[5],
                                         aRide1[6], aRide1[7])

                    standardRideList.deleteAt(n)
                    addUser(standardRideList, temp)
    # sort Shared List


def sortsharedList(list):
    for m in range(list.size() - 1, 0, -1):
        for n in range(m):
            #
            sRide1 = splitString(str(sharedList.showDetail(int(n))))
            sRide2 = splitString(str(sharedList.showDetail(int(n + 1))))

            if (sRide2[0] is not None):
                # delete the entry and add it to the end
                if sRide1[0] > sRide2[0]:
                    temp = SharedRides(sRide1[0], sRide1[1], sRide1[2], sRide1[3], sRide1[4], sRide1[5],
                                         sRide1[6], sRide1[7], sRide1[8], sRide1[9])

                    standardRideList.deleteAt(n)
                    addUser(standardRideList, temp)


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
    return km


def findRideIndex(list, smallest, size, userId):  # uses binary search

    # def binarySearch(arr, l, r, x): #l = first value r = last val x = value we searching
    if size > smallest:
        mid = smallest + (size - smallest) / 2
        currentId = splitString(str(list.showDetail(mid)))
        if currentId[0] is None or 0 <= int(mid) <= 1:
            return 0

        # returns mid value
        elif int(currentId[0]) == int(userId):
            return mid

        elif int(currentId[0]) > int(userId):
            return findRideIndex(list, smallest, mid - 1, userId)

        else:

            return findRideIndex(list, mid + 1, size, userId)
    else:
        return 0


def endRide(request):
    userId = request.user.id

    listStored = findList(userId)

    # for Shared Rides
    if int(listStored) == 1:
        position = findRideIndex(sharedList, 0, sharedList.size() - 1, userId)
        position = math.ceil(int(position))
        sharedList.deleteAt(position)
        uTable.delVal(userId)
        ended = "Shared Ride Has Ended"
        return JsonResponse(ended, safe=False)

        # for Accepted Rides
    elif int(listStored) == 2:
        position = findRideIndex(standardRideList, 0, standardRideList.size() - 1, userId)
        position = math.ceil(int(position))
        standardRideList.deleteAt(int(position))
        uTable.delVal(userId)
        ended = "Normal Ride Has Ended"
        return JsonResponse(ended, safe=False)

        # for when shared rides is chosen but no other riders are nearby
    elif int(listStored) == 3:
        mainId = findMainRider(sharedList, userId)
        position = findRideIndex(sharedList, 0, sharedList.size() - 1, mainId)
        position = math.ceil(int(position))
        sharedList.deleteAt(position)
        uTable.delVal(mainId)
        uTable.delVal(userId)
        ended = "Shared Ride Has Ended"
        return JsonResponse(ended, safe=False)


# creating all the Linked List and functions we will use

# Linked List for Drivers
driverList = models.Drivers.objects.all()

# Linked List for Rider
passengerList = createList()

# Linked List for Accepted Rides
standardRideList = createList()

# Linked List for Shared Rides
sharedList = createList()

# Hash Table for sharing of rides
uTable = HashTable()

Rider2 = riderRequest("2103", "1.4240477,103.8390045", "1331522", "1.4410467,103.839182", 31023, 1,
                      '20')

