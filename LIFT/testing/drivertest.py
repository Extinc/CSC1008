class Driver:
  def __init__(self, userId, driverLocation,typeOfCar,status):
    self.userId = userId
    self.driverLocation = driverLocation
    self.typeOfCar = typeOfCar
    self.status = status

class riderRequest:
  def __init__(self, passengerId,pickUpLocation,pickUpTime,destination,rideDistance,typeOfCar,status,type):
    self.passengerId= passengerId
    self.pickUpLocation = pickUpLocation
    self.pickUpTime =pickUpTime
    self.destination = destination
    #self.rideDistance = getRideDistance(pickUpLocation,destination)#in meter
    self.rideDistance = rideDistance
    self.price = "300"
    #self.price = getPrice(rideDistance,typeOfCar)
    self.typeOfCar = typeOfCar
    self.status = status
    self.type = type

    def getRideDistance(pickUpLocation,destination):
      distance = destination-pickUpLocation #example only
      return distance

    def getPrice(distance,typeOfCar):
        price = 3 #standard price for less than 1km
        distance-=1000
        if distance<10000: #up to 10+1km
          while distance>0:
            price+=0.22
            distance-=400 #every 400m
        elif distance>10000: #10+1+remainingkm
          distance-10000
          price+=0.22*25 #25x400 =10000
          while distance>0:
            price+=0.22
            distance -=350 #every 350m
        if typeOfCar == "8 Seater" :
          price*=1.5
        return price



class AcceptedRides:
    def __init__(self, passengerId,pickUpLocation,driverLocation,pickUpTime,destination,rideDistance,price,typeOfCar,driverId):
        self.passengerId= passengerId
        self.pickUpLocation = pickUpLocation
        self.pickUpTime =pickUpTime
        self.destination = destination
        #self.driverDistance = getDriverDistance(driverLocation,pickUpLocation)
        self.rideDistance = rideDistance
        self.price = price
        self.typeOfCar = typeOfCar
        self.driverId = driverId

        def getDriverDistance(driverLocation,pickUpLocation):
            return driverLocation-pickUpLocation

        def getDriverDistance(driverLocation, pickUpLocation):
            pass

class sharedRides:
    def __init__(self, p1Id,p2Id, startLocation,loc2,loc3,finalLocation,driverLocation,pickUpTime,typeOfCar,driverId):
        self.p1Id= p1Id
        self.p2Id = p2Id
        self.startLocation = startLocation
        self.loc2 = loc2
        self.loc3 = loc3
        self.finalLocation = finalLocation
        #self.driverDistance = getDriverDistance(driverLocation,pickUpLocation)
        self.pickUpTime =pickUpTime
        self.typeOfCar = typeOfCar
        self.driverId = driverId
        pass

class Node:
    def __init__(self,driver):
        details = driver.__dict__
        d = details.values()
        list = ' '.join(str(val) for val in d)
        
        # while i<count:
        #     set = details.popitem()
        #     var = set[0]
        #     val= set[1]
        #     setattr(self,var,val) #equivalent to self.var = val
            
        #     i+=1
        self.next = None
        self.list = list

class SinglyLinkedList:
    def __init__(self):
        self.head = None
    #return the value of the node at index

    def search(self, index):
        temp = self.head
        prev = None
        counter = 0
        while temp is not None and counter < index:
            prev = temp
            temp = temp.next
            counter += 1

        if temp is None:
            print('search error: invalid index')
        else:
            return temp
    def insertAtEnd(self, object):
      NewNode = Node(object)
      if self.head is None:
         self.head = NewNode
         return
      laste = self.head
      while(laste.next):
         laste = laste.next
      laste.next=NewNode

    def insertAtHead(self, node):
        if self.head is None:
            self.head = node
        else:
            node.next = self.head
            self.head = node

    def delete(self, value):
        prev = None
        temp = self.head

        while temp != None and temp.data != value:
            prev = temp
            temp = temp.next

        #node to be deleted is head
        if temp == self.head:
            self.deleteAtHead()

        #Value found
        elif temp != None:
            prev.next = temp.next
            del temp
        #Value not found
        else:
            print('Value ', value, ' cannot be found')

    #delete the node at index
    def deleteAt(self,index):
        temp = self.head
        prev = None
        counter = 0
        while temp is not None and counter < index:
            prev = temp
            temp = temp.next
            counter += 1

        if temp is None:
            print('search error: invalid index')
        else:
            if prev is None:
                self.head = temp.next
            else:
                prev.next = temp.next
            del temp

    def deleteAtHead(self):
        temp = self.head
        self.head = self.head.next
        del temp

    def printList(self):
        output = "Current list content: [ "
        temp = self.head
        while temp is not None:
            output += str(temp.list) + ","
            temp = temp.next
        output += "]"
        print(output)

    def printDetail(self,index):
        temp = self.head
        prev = None
        counter = 0
        while temp is not None and counter < index:
            prev = temp
            temp = temp.next
            counter += 1

        if temp is None:
            print('search error: invalid index')
        else:
            if prev is None:
                self.head = temp.next
            else:
                prev.next = temp.next
            print(temp.list)
            return temp.list
        

    #return the number of elements in the queue
    def size(self):
        temp = self.head
        if temp is not None:
            size = 1
        else:
            size = 0
        while temp is not None:
            size += 1
            temp = temp.next
        return size

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
                newSR = sharedRides(firstRider[0],nextRider[0],firstRider[1],firstRider[3],nextRider[1],nextRider[3],"driver Location",firstRider[2],firstRider[5],"driverId") #for when its destination is closer to first rider so car goes from 
            if pToD>pToP:
                newSR = sharedRides(firstRider[0],nextRider[0],firstRider[1],nextRider[1],firstRider[3],nextRider[3],"driver Location",firstRider[2],firstRider[5],"driverId") #normal case where it picks up passenger along the way
        addUser(sList,newSR)
        print("New Shared Ride",sList.printDetail(0))

def distance(location1,location2):
    if int(location1) >= int(location2):
        distance = int(location1) - int(location2)
    else:
        distance = int(location2)-int(location1)
    print("distance",distance)
    return distance  


dList =createUserList()

#retrieve ID based on account

DRW1923 = Driver("DRW1923",128012,8,"Finding Rider")
rList = createUserList()
FES2103 = riderRequest("FES2103",2819102,"1331522",3928181,31023,8,"Finding Driver","Shared")
FES2211 = riderRequest("FES2211",2819102,"1331522",3928181,31023,8,"Finding Driver","Shared")
addUser(rList,FES2103)
addUser(rList,FES2211)
addUser(dList,DRW1923)

aList = createUserList()
SQE762812=AcceptedRides(FES2103.passengerId,FES2103.pickUpLocation,DRW1923.driverLocation,FES2103.pickUpTime,FES2103.destination,FES2103.rideDistance,FES2103.price,FES2103.typeOfCar,DRW1923.userId)
SQ2312812=AcceptedRides(FES2103.passengerId,FES2103.pickUpLocation,DRW1923.driverLocation,FES2103.pickUpTime,FES2103.destination,FES2103.rideDistance,FES2103.price,FES2103.typeOfCar,DRW1923.userId)
rmList = createUserList() #rider match
addUser(rmList,SQE762812) #test
addUser(rmList,SQ2312812) #ticles
sList = createUserList()
print("test2",rmList.size())
#firstRider = splitString(str(mList.printDetail(0)))
#print(firstRider[1]) #print first rider pick up location

findNearestRider(rList,sList)#pass in 




