import math
from multiprocessing import shared_memory


class HashTable:
  
    # Create empty bucket list of given size
    def __init__(self):
        self.size = 1000
        self.hash_table = self.create_buckets()
  
    def create_buckets(self):
        return [[] for _ in range(self.size)]
  
    # Insert values into hash map
    def setVal(self, key, val):
        
        # Get the index from the key
        # using hash function
        hashed_key = hash(key) % self.size
          
        # Get the bucket corresponding to index
        bucket = self.hash_table[hashed_key]
  
        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record
              
            # check if the bucket has same key as
            # the key to be inserted
            if record_key == key:
                found_key = True
                break
  
        # If the bucket has same key as the key to be inserted,
        # Update the key value
        # Otherwise append the new key-value pair to the bucket
        if found_key:
            bucket[index] = (key, val)
        else:
            bucket.append((key, val))
  
    # Return searched value with specific key
    def getVal(self, key):
        
        # Get the index from the key using
        # hash function
        hashed_key = hash(key) % self.size
          
        # Get the bucket corresponding to index
        bucket = self.hash_table[hashed_key]
  
        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record
              
            # check if the bucket has same key as 
            # the key being searched
            if record_key == key:
                found_key = True
                break
  
        # If the bucket has same key as the key being searched,
        # Return the value found
        # Otherwise indicate there was no record found
        if found_key:
            return record_val
        else:
            return "No record found"
  
    # Remove a value with specific key
    def delVal(self, key):
        
        # Get the index from the key using
        # hash function
        hashed_key = hash(key) % self.size
          
        # Get the bucket corresponding to index
        bucket = self.hash_table[hashed_key]
  
        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record
              
            # check if the bucket has same key as
            # the key to be deleted
            if record_key == key:
                found_key = True
                break
        if found_key:
            bucket.pop(index)
        return
  
    # To print the items of hash map
    def __str__(self):
        return "".join(str(item) for item in self.hash_table)
  
  

class Driver:
  def __init__(self, userId, driverLocation,seatNo):
    self.userId = userId
    self.driverLocation = driverLocation
    self.seatNo = seatNo

class riderRequest:
  def __init__(self, passengerId,pickUpLocation,pickUpTime,destination,rideDistance,seatNo,price):
    self.passengerId= passengerId
    self.pickUpLocation = pickUpLocation
    self.pickUpTime =pickUpTime
    self.destination = destination
    #self.rideDistance = getRideDistance(pickUpLocation,destination)#in meter
    self.rideDistance = rideDistance
    #self.price = getPrice(rideDistance,typeOfCar)
    self.seatNo = seatNo
    self.price = price

    



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
    def insertAt(self, object, index):     

        #1. allocate node to new element
        newNode = Node(object)

        #2. check if the index is > 0 
        if(index < 1):
            print("\nindex should be >= 1.")
        elif (index == 1):

        #3. if the index is 1, make next of the
        #   new node as head and new node as head
            newNode.next = self.head
            self.head = newNode
        else:    

            #4. Else, make a temp node and traverse to the 
            #   node previous to the index
            temp = self.head
            for i in range(1, index-1):
                if(temp != None):
                    temp = temp.next   

            #5. If the previous node is not null, make 
            #   newNode next as temp next and temp next 
            #   as newNode.
            if(temp != None):
                newNode.next = temp.next
                temp.next = newNode  
            else:

                #6. When the previous node is null
                print("\nThe previous node is null.")  
        

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

    def listDetail(self,index): #pop
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

    def isEmpty(self):
        current_node = self.head
        return current_node == None
        
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
                uTable.setVal(firstRider[0],"1") #sharedRide = 1, AcceptedRides = 2. We just need to store an ID for one user since its a shared ride
                print("New Shared Ride",sList.size())
            else:
                newSR = SharedRides(firstRider[0],nextRider[0],firstRider[1],nextRider[1],firstRider[3],nextRider[3],driver[1],firstRider[2],firstRider[5],driver[0]) #normal case where it picks up passenger along the way
                
                addUser(sList,newSR)
                uTable.setVal(firstRider[0],"1")
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
                        uTable.setVal(rider[0],"2")
                        dList.deleteAt(x)
                        rList.deleteAt(0)
                elif(int(rider[5]) == int(5) or int(rider[5]) == int(8)):
                    if int(rider[5]) == int(driver[2]):
                        newRide = AcceptedRides(rider[0],rider[1],driver[1],rider[2],rider[3],rider[4],rider[6],rider[5],driver[0])
                        print(aList.size())
                        size = aList.size()-2
                        if int(size) > 0:
                            print("size is",aList.size())
                            print("alist",aList.listDetail(size()-1))
                            for ii in range(0,size):
                                currentrider = splitString(str(aList.listDetail(int(ii))))
                                print("current rider is",currentrider[0])
                                print("rider is",rider[0])
                                if int(rider[0]) > int(currentrider[0]):
                                    print("ii",ii)
                                    aList.insertAt(newRide,ii-1)
                                    break
                        else:
                            aList.insertAtHead(newRide)
                        uTable.setVal(rider[0],"2")
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
        
        
def findList(userId,sList,aList): #uses binary search
    listStored = uTable.getVal(userId)
    if int(listStored) == 1:
        print(sList.size())
        position = findRideIndex(sList,0,sList.size()-1,userId)
        return math.ceil(position)
        
        
    elif int(listStored) ==2:
        print(aList.size())
        position = findRideIndex(aList,0,aList.size()-1,userId)
        return math.ceil(position)
        
    


def findRideIndex(list,smallest,size,userId):
    #def binarySearch(arr, l, r, x): #l = first value r = last val x = value we searching
    if size >= smallest:
        mid = smallest + (size-smallest)/2
        print(mid)
        print(size)
        currentId = splitString(str(list.listDetail(mid)))
        print(currentId[0])
        if int(currentId[0]) == int(userId):
            print("mid",mid)
            return mid
        
        elif int(currentId[0]) > int(userId):
            return findRideIndex(list,smallest,mid-1,userId)
        
        else:
                
            return findRideIndex(list,mid+1,size,userId)
        
    



    



def distanceCalculation(startLocation, endLocation):
    startLocation = startLocation.split(',')
    return 4999


dList =createUserList()

#retrieve ID based on account

DRW1923 = Driver("DRW1923",2819041,8)
DRW1911 = Driver("DRW1911",2819041,8)
DRW1915 = Driver("DRW1915",2819041,8)
DRW1922 = Driver("DRW1922",2819041,8)
rList = createUserList()
FES2103 = riderRequest("2103",2819102,"1331522",3928181,31023,8,'20')
FES2244 = riderRequest("2244",2819102,"1331522",3928181,31023,8,'20')
FES2211 = riderRequest("2211",2819102,"1331522",3928181,31023,8,'20')
FES2152 = riderRequest("2152",2819102,"1331522",3928181,31023,8,'20')
FES2112 = riderRequest("2112",2819102,"1331522",3928181,31023,8,'20')
FES1812 = riderRequest("1812",2819102,"1331522",3928181,31023,8,'20')
addUser(rList,FES1812)
addUser(rList,FES2103)
addUser(rList,FES2112)
addUser(rList,FES2152)
addUser(rList,FES2152)
addUser(rList,FES2152)
addUser(rList,FES2152)
addUser(rList,FES2152)
addUser(rList,FES2152)
addUser(rList,FES2152)
addUser(rList,FES2152)
addUser(rList,FES2152)
addUser(rList,FES2211)
addUser(rList,FES2244)


addUser(rList,FES2244)


addUser(rList,FES2244)
addUser(dList,DRW1915)
addUser(dList,DRW1915)
addUser(dList,DRW1915)
addUser(dList,DRW1923)
addUser(dList,DRW1915)
addUser(dList,DRW1923)

addUser(dList,DRW1915)
addUser(dList,DRW1915)
addUser(dList,DRW1923)
addUser(dList,DRW1915)
addUser(dList,DRW1923)

addUser(dList,DRW1915)
addUser(dList,DRW1915)
addUser(dList,DRW1923)
addUser(dList,DRW1915)
addUser(dList,DRW1923)


uTable = HashTable()

aList = createUserList() #accepted rides List
rmList = createUserList() #rider match
sList = createUserList()
#firstRider = splitString(str(mList.printDetail(0)))
#print(firstRider[1]) #print first rider pick up location

findRides(rList,dList,aList,sList)
print("accepted",aList.listDetail(0))
print("accepted",aList.listDetail(1))
print("accepted",aList.listDetail(2))
print("accepted",aList.listDetail(3))
print("accepted",aList.listDetail(4))
print("accepted",aList.listDetail(5))


print("shared",sList.listDetail(0))
print("shared",sList.listDetail(1))



#removal of data
#adding of driver 
#finding based on seat and type of car




