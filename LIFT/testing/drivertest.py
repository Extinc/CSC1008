class Driver:
  def __init__(self, userId, driverLocation,typeOfCar,status):
    self.userId = userId
    self.driverLocation = driverLocation
    self.typeOfCar = typeOfCar
    self.status = status

class riderRequest:
  def __init__(self,rideId, passengerId,pickUpLocation,pickUpTime,destination,rideDistance,typeOfCar,status):
    self.rideId = rideId
    self.passengerId= passengerId
    self.pickUpLocation = pickUpLocation
    self.pickUpTime =pickUpTime
    self.destination = destination
    #self.rideDistance = getRideDistance(pickUpLocation,destination)#in meter
    #self.price = getPrice(rideDistance,typeOfCar)
    self.typeOfCar = typeOfCar
    self.status = status

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

    #return the number of elements in the queue
    def size(self):
        temp = self.head
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

dList =createUserList()
DRW1923 = Driver("DRW1923",128012,8,"Finding Rider")
rList = createUserList()
FES2103 = riderRequest("SQE762812","FES2103",2819102,"1331522",3928181,31023,8,"Finding Driver")

addUser(rList,FES2103)
addUser(dList,DRW1923)

