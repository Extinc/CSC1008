from LIFT.codes.AcceptedRides import AcceptedRides
from LIFT.codes.SharedRides import SharedRides
from LIFT.datastructure.linkedList import SinglyLinkedList
from LIFTMAIN.settings import ONEMAP_DEV_URL, ONEMAP_TOKEN
import requests



def createUserList():
    userList =  SinglyLinkedList()
    return userList

def addUser(userList,object):
    userList.insertAtEnd(object)
    userList.printList()

def splitString(userString):
    return str(userString).split(' ')

def findNearestRider(rList,sList,driver):
    firstRider = splitString(str(rList.listDetail(0)))
    for i in range(1,rList.size()-1):
        nextRider = splitString(str(rList.listDetail(int(i))))
        pToP =distance(firstRider[1],nextRider[1]) #compare pickup for rider 1 and next rider
        pToD = distance(firstRider[3],nextRider[1]) #compare dropoff for rider 1 and pickup for rider2
        if(int(pToP) <5000 or int(pToD)<5000 and int(nextRider[5])==1): #check if in range
            if pToP>=pToD: 
                newSR = SharedRides(firstRider[0],nextRider[0],firstRider[1],firstRider[3],nextRider[1],nextRider[3],"driver Location",firstRider[2],firstRider[5],driver[0]) #for when its destination is closer to first rider so car goes from 
            if pToD>pToP:
                newSR = SharedRides(firstRider[0],nextRider[0],firstRider[1],nextRider[1],firstRider[3],nextRider[3],"driver Location",firstRider[2],firstRider[5],driver[0]) #normal case where it picks up passenger along the way
            addUser(sList,newSR)
            print("New Shared Ride",sList.listDetail(i))
            rList.deleteAt(i)
            break

def findRides(rList,dList,aList,sList): #aList =Accepted Rides sList= Shared Rides rList = ridersList
    rider = splitString(str(rList.listDetail(int(0)))) #retrieve first rider details

    for x in range(0,dList.size()-1):
        
        driver = splitString(str(dList.listDetail(int(x))))
        print("driver test",str(driver))
        if str(driver) != "Not Found":
            if distance(driver[1],rider[1]) <5000:
                if int(rider[5]) == 1:
                    findNearestRider(rList,sList,driver)
                    dList.deleteAt(x)
                    rList.deleteAt(0)
                    break
                elif(int(rider[5]) == int(5) or int(rider[5]) == int(8)):
                    if int(rider[5]) == int(driver[2]):
                        newRide = AcceptedRides(rider[0],rider[1],driver[1],rider[2],rider[3],rider[4],"200",rider[5],driver[0])
                        addUser(aList,newRide)
                        dList.deleteAt(x)
                        rList.deleteAt(0)
                        break
                else:
                    print("no same seat")
                break
        else:
            print("Driver Not Found")
        
                

def distance(location1,location2):
    if int(location1) >= int(location2):
        distance = int(location1) - int(location2)
    else:
        distance = int(location2)-int(location1)
    print("distance",distance)
    return distance  
        
    #print("rider test",rider)
        
def distanceCalculation(startLocation, endLocation):
    urls = ONEMAP_DEV_URL+ "/privateapi/routingsvc/route"
    params ={}
    params["start"] = str(startLocation)
    params["end"] = str(endLocation)
    params["routeType"] = "drive"
    params['token'] = ONEMAP_TOKEN
    response = requests.get(urls, params=params)
    #print(response.json()["route_summary"]["total_distance"])
    totaldistance = response.json()["route_summary"]["total_distance"]
    print("totaldistance is : " + str(totaldistance))
    return totaldistance