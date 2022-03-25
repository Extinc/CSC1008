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
    print("driver deets",driver)
    for i in range(1,rList.size()-1):
        nextRider = splitString(str(rList.listDetail(int(i))))
        pToP =distanceCalculation(firstRider[1],nextRider[1]) #compare pickup for rider 1 and next rider
        pToD = distanceCalculation(firstRider[3],nextRider[1]) #compare dropoff for rider 1 and pickup for rider2
        if(int(pToP) <5000 or int(pToD)<5000 and int(nextRider[5])==1): #check if in range
            if pToP>=pToD: 
                newSR = SharedRides(firstRider[0],nextRider[0],firstRider[1],firstRider[3],nextRider[1],nextRider[3],driver[1],firstRider[2],firstRider[5],driver[0]) #for when its destination is closer to first rider so car goes from 
                addUser(sList,newSR)
                print("New Shared Ride",sList.size())
            else:
                newSR = SharedRides(firstRider[0],nextRider[0],firstRider[1],nextRider[1],firstRider[3],nextRider[3],driver[1],firstRider[2],firstRider[5],driver[0]) #normal case where it picks up passenger along the way
                
                addUser(sList,newSR)
                print("New Shared Ride",sList.size())
                

            print("New Shared Ride",sList.listDetail(int(sList.size()-2)))
            rList.deleteAt(i)
            return True
            
        return False

def findRides(rList,dList,aList,sList): #aList =Accepted Rides sList= Shared Rides rList = ridersList
    rider = splitString(str(rList.listDetail(int(0)))) #retrieve first rider details
    if(dList.size()>0):
        for x in range(0,dList.size()-1):
            
            driver = splitString(str(dList.listDetail(int(x))))
            if distanceCalculation(driver[1],rider[1]) <5000:
                if int(rider[5]) == 1:
                    sharedCheck = findNearestRider(rList,sList,driver)
                    if sharedCheck == True:
                        dList.deleteAt(x)
                        rList.deleteAt(0)
                        break
                    else:
                        print("No Shared Ride Found")
                        newRide = AcceptedRides(rider[0],rider[1],driver[1],rider[2],rider[3],rider[4],rider[6],rider[5],driver[0])
                        addUser(aList.newRide)
                        dList.deleteAt(x)
                        rList.deleteAt(0)
                elif(int(rider[5]) == int(5) or int(rider[5]) == int(8)):
                    if int(rider[5]) == int(driver[2]):
                        newRide = AcceptedRides(rider[0],rider[1],driver[1],rider[2],rider[3],rider[4],rider[6],rider[5],driver[0])
                        addUser(aList,newRide)
                        dList.deleteAt(x)
                        rList.deleteAt(0)
                        break
                else:
                    print("no same seat")
                break
    else:
        print("Driver Not Found")
    
    if dList.size()>0 and rList.size()>0:
        findRides(rList,dList,aList,sList)   #recursive until there are no more riders or drivers
        
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

dList =createUserList()
rList = createUserList()
aList = createUserList()
sList = createUserList()