from lib2to3.pgen2 import driver
from App.classes.AcceptedRides import AcceptedRides
from App.classes.Driver import Driver
from App.classes.UserRequest import UserRequest


class Matched:
    FES2103 = UserRequest("SQE762812","FES2103",2819102,"1331522",3928181,31023,8,"Finding Driver") #userId is used to make object
    DRW1923 = Driver("DRW1923",128012,8,"Finding Rider") #userId is used to make object
    

    #when ride is accepted
    FES2103.status = "In Ride"
    DRW1923.status = "Busy"
    FES2103.rideId = AcceptedRides(FES2103.rideId,"FES2103",2819102,"1331522",3928181,5231,31023,FES2103.price,8,"DRW1923")
