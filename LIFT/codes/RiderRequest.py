class RiderRequest:
  def __init__(self, passengerId,pickUpLocation,pickUpTime,destination,rideDistance,typeOfCar,rideType):
    self.passengerId= passengerId
    self.pickUpLocation = pickUpLocation
    self.pickUpTime =pickUpTime
    self.destination = destination
    #self.rideDistance = getRideDistance(pickUpLocation,destination)#in meter
    self.rideDistance = rideDistance
    self.price = "300"
    #self.price = getPrice(rideDistance,typeOfCar)
    self.typeOfCar = typeOfCar
    self.rideType = rideType

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