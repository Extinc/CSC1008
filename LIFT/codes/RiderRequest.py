
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
