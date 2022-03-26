# Create your models here.
from django.db import models


class PointInfo(models.Model):
    BUILDINGNAME = models.CharField(max_length=250, null=True)
    BLOCK = models.CharField(max_length=250, null=True)
    ROAD = models.CharField(max_length=250, null=True)
    FEATURENAME = models.CharField(max_length=250, null=True)
    POSTALCODE = models.CharField(max_length=250, null=True)
    HIGHWAY = models.TextField(null=True)
    lat = models.FloatField(default=0)
    long = models.FloatField(default=0)

    def __str__(self):
        return '{} {} {} '.format(self.id, self.BUILDINGNAME, self.POSTALCODE)


class PathCache(models.Model):
    source = models.TextField(null=False)
    destination = models.TextField(null=False)
    Data = models.TextField(null=True, primary_key=False)
    DateTime = models.DateTimeField()


class Drivers(models.Model):
    id = models.AutoField(primary_key=True)
    driverID = models.IntegerField(default=0)
    name = models.TextField(null=False)
    driverlat = models.FloatField(default=0)
    driverlong = models.FloatField(default=0)
    seatNo = models.IntegerField(default=0)
    status = models.TextField(null=False)