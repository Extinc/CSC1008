class AcceptedRides:
    def __init__(self, passengerId, pickUpLocation, driverLocation, pickUpTime, destination, rideDistance, price,
                 seatNo, driverId):
        self.passengerId = passengerId
        self.pickUpLocation = pickUpLocation
        self.pickUpTime = pickUpTime
        self.destination = destination
        # self.driverDistance = getDriverDistance(driverLocation,pickUpLocation)
        self.rideDistance = rideDistance
        self.price = price
        self.seatNo = seatNo
        self.driverId = driverId
