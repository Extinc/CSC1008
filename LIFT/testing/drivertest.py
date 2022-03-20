class Driver:
  def __init__(self, userId, driverLocation,seatNo):
    self.userId = userId
    self.driverLocation = driverLocation
    self.seatNo = seatNo

class riderRequest:
  def __init__(self, passengerId,pickUpLocation,pickUpTime,destination,rideDistance,seatNo):
    self.passengerId= passengerId
    self.pickUpLocation = pickUpLocation
    self.pickUpTime =pickUpTime
    self.destination = destination
    #self.rideDistance = getRideDistance(pickUpLocation,destination)#in meter
    self.rideDistance = rideDistance
    #self.price = getPrice(rideDistance,typeOfCar)
    self.seatNo = seatNo

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
        if seatNo == 8 :
          price*=1.5
        return price



class AcceptedRides:
    def __init__(self, passengerId,pickUpLocation,driverLocation,pickUpTime,destination,rideDistance,price,seatNo,driverId):
        self.passengerId= passengerId
        self.pickUpLocation = pickUpLocation
        self.pickUpTime =pickUpTime
        self.destination = destination
        #self.driverDistance = getDriverDistance(driverLocation,pickUpLocation)
        self.rideDistance = rideDistance
        self.price = price
        self.seatNo = seatNo
        self.driverId = driverId

        def getDriverDistance(driverLocation,pickUpLocation):
            return driverLocation-pickUpLocation

        def getDriverDistance(driverLocation, pickUpLocation):
            pass

class SharedRides:
    def __init__(self, p1Id,p2Id, startLocation,loc2,loc3,finalLocation,driverLocation,pickUpTime,seatNo,driverId):
        self.p1Id= p1Id
        self.p2Id = p2Id
        self.startLocation = startLocation
        self.loc2 = loc2
        self.loc3 = loc3
        self.finalLocation = finalLocation
        #self.driverDistance = getDriverDistance(driverLocation,pickUpLocation)
        self.pickUpTime =pickUpTime
        self.seatNo = seatNo
        self.driverId = driverId
        

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

    def insertAtHead(self, object):
        NewNode = Node(object)
        if self.head is None:
            self.head = NewNode
        else:
            NewNode.next = self.head
            self.head = NewNode

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

    def printDetail(self,index): #pop
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

def findNearestRider(rList,sList,driver):
    firstRider = splitString(str(rList.printDetail(0)))
    for i in range(1,rList.size()-1):
        nextRider = splitString(str(rList.printDetail(int(i))))
        pToP =distance(firstRider[1],nextRider[1]) #compare pickup for rider 1 and next rider
        pToD = distance(firstRider[3],nextRider[1]) #compare dropoff for rider 1 and pickup for rider2
        if(int(pToP) <5000 or int(pToD)<5000 and int(nextRider[5])==1): #check if in range
            if pToP>=pToD: 
                newSR = SharedRides(firstRider[0],nextRider[0],firstRider[1],firstRider[3],nextRider[1],nextRider[3],"driver Location",firstRider[2],firstRider[5],driver[0]) #for when its destination is closer to first rider so car goes from 
            if pToD>pToP:
                newSR = SharedRides(firstRider[0],nextRider[0],firstRider[1],nextRider[1],firstRider[3],nextRider[3],"driver Location",firstRider[2],firstRider[5],driver[1]) #normal case where it picks up passenger along the way
            addUser(sList,newSR)
            print("New Shared Ride",sList.printDetail(i))
            rList.deleteAt(i)
            break

def findRides(rList,dList,aList,sList): #aList =Accepted Rides sList= Shared Rides rList = ridersList
    rider = splitString(str(rList.printDetail(int(0)))) #retrieve first rider details
    for x in range(0,dList.size()-1):
        print(x)
        driver = splitString(str(dList.printDetail(int(x))))
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
                


         
        #print("rider test",rider)
        



        

            



        
    

def distance(location1,location2):
    if int(location1) >= int(location2):
        distance = int(location1) - int(location2)
    else:
        distance = int(location2)-int(location1)
    print("distance",distance)
    return distance  


dList =createUserList()

#retrieve ID based on account

DRW1923 = Driver("DRW1923",2819041,8)
DRW1911 = Driver("DRW1911",2819041,8)
DRW1915 = Driver("DRW1915",2819041,8)
DRW1922 = Driver("DRW1922",2819041,8)
rList = createUserList()
FES2103 = riderRequest("FES2103",2819102,"1331522",3928181,31023,8)
FES2244 = riderRequest("FES2244",2819102,"1331522",3928181,31023,8)
FES2211 = riderRequest("FES2211",2819102,"1331522",3928181,31023,1)
FES2152 = riderRequest("FES2152",2819102,"1331522",3928181,31023,1)
FES2112 = riderRequest("FES2112",2819102,"1331522",3928181,31023,1)
FES1812 = riderRequest("FES1812",2819102,"1331522",3928181,31023,1)
addUser(rList,FES2103)
addUser(rList,FES2211)
addUser(rList,FES2152)
addUser(rList,FES2244)
addUser(rList,FES2112)
addUser(rList,FES1812)
addUser(dList,DRW1923)
addUser(dList,DRW1911)
addUser(dList,DRW1915)
addUser(dList,DRW1922)



aList = createUserList() #accepted rides List
rmList = createUserList() #rider match
sList = createUserList()
#firstRider = splitString(str(mList.printDetail(0)))
#print(firstRider[1]) #print first rider pick up location

findRides(rList,dList,aList,sList)
findRides(rList,dList,aList,sList)
findRides(rList,dList,aList,sList)
findRides(rList,dList,aList,sList)
print("accepted",aList.printDetail(0))
print("accepted",aList.printDetail(1))

print("shared",sList.printDetail(0))
print("shared",sList.printDetail(1))
#removal of data
#adding of driver 
#finding based on seat and type of car




