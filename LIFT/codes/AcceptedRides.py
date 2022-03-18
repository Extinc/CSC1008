


class AcceptedRides:
  def __init__(self, passengerId,pickUpLocation,driverLocation,pickUpTime,destination,rideDistance,price,typeOfCar,driverId,type):
    self.passengerId= passengerId
    self.pickUpLocation = pickUpLocation
    self.pickUpTime =pickUpTime
    self.destination = destination
    self.driverDistance = getDriverDistance(driverLocation,pickUpLocation)
    self.rideDistance = rideDistance
    self.price = price
    self.typeOfCar = typeOfCar
    self.driverId = driverId
    self.type = type

    def getDriverDistance(driverLocation,pickUpLocation):
      return driverLocation-pickUpLocation

    def getDriverDistance(driverLocation, pickUpLocation):
      pass