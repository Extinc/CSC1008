class SharedRides:
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