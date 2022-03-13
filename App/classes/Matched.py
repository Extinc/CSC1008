from lib2to3.pgen2 import driver
from App.classes.AcceptedRides import AcceptedRides
from App.classes.Driver import Driver
from App.classes.UserRequest import UserRequest


class Matched:
    FES2103 = UserRequest("SQE762812","FES2103",2819102,"1331522",3928181,31023,8,"Finding Driver") #userId is used to make object
    DRW1923 = Driver("DRW1923",128012,8,"Finding Rider") #userId is used to make object
    
    if FES2103.pickUpLocation-DRW1923.driverLocation < 5000 and DRW1923.status is True and FES2103.status is True: #if it meets location criteria and if both passenger driver is not busy
      #when ride is accepted
      FES2103.status = False
      DRW1923.status = False
      FES2103.rideId = AcceptedRides(FES2103.rideId,FES2103.passengerId,FES2103.pickUpLocation,DRW1923.driverLocation,FES2103.pickUpTime,FES2103.destination,FES2103.rideDistance,FES2103.price,FES2103.typeOfCar,DRW1923.userId)
