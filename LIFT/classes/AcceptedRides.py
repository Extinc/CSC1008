class AcceptedRides:
  def __init__(self, rideId,passengerId,pickUpLocation,driverLocation,pickUpTime,destination,rideDistance,price,typeOfCar,driverId):
    self.rideId = rideId
    self.passengerId= passengerId
    self.pickUpLocation = pickUpLocation
    self.pickUpTime =pickUpTime
    self.destination = destination
    self.driverDistance = getDriverDistance(driverLocation,pickUpLocation)
    self.rideDistance = rideDistance
    self.price = price
    self.typeOfCar = typeOfCar
    self.driverId = driverId

    def getDriverDistance(driverLocation,pickUpLocation):
      return driverLocation-pickUpLocation