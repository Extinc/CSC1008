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
