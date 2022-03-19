from LIFT.codes.SharedRides import SharedRides
from LIFT.datastructure.linkedList import SinglyLinkedList



def createUserList():
    userList =  SinglyLinkedList()
    return userList

def addUser(userList,object):
    userList.insertAtEnd(object)
    userList.printList()
    
def splitString(userString):
    return str(userString).split(' ')

def findNearestRider(object,sList):
    firstRider = splitString(str(object.printDetail(0)))
    nextRider = splitString(str(object.printDetail(1)))
    print("test",nextRider)
    
    for i in range(0,object.size()-1):
        print(i)
        nextRider = splitString(str(object.printDetail(int(i))))
        pToP =distance(firstRider[1],nextRider[1]) #compare pickup for rider 1 and next rider
        pToD = distance(firstRider[3],nextRider[1]) #compare dropoff for rider 1 and pickup for rider2
        if(int(pToP) <5000 or int(pToD)<5000):
            if pToP>=pToD:
                newSR = SharedRides(firstRider[0],nextRider[0],firstRider[1],firstRider[3],nextRider[1],nextRider[3],"driver Location",firstRider[2],firstRider[5],"driverId") #for when its destination is closer to first rider so car goes from 
            if pToD>pToP:
                newSR = SharedRides(firstRider[0],nextRider[0],firstRider[1],nextRider[1],firstRider[3],nextRider[3],"driver Location",firstRider[2],firstRider[5],"driverId") #normal case where it picks up passenger along the way
        addUser(sList,newSR)
        print("New Shared Ride",sList.printDetail(0))

def distance(location1,location2):
    if int(location1) >= int(location2):
        distance = int(location1) - int(location2)
    else:
        distance = int(location2)-int(location1)
    print("distance",distance)
    return distance  