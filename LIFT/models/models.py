# Create your models here.
from django.db import models


class PointInfo(models.Model):
    BUILDINGNAME = models.CharField(max_length=250, null=True)
    BLOCK = models.CharField(max_length=250, null=True)
    ROAD = models.CharField(max_length=250, null=True)
    FEATURENAME = models.CharField(max_length=250, null=True)
    POSTALCODE = models.CharField(max_length=250, null=True)
    HIGHWAY = models.TextField(null=True)
    def __str__(self):
        return '{} by {}'.format(self.BUILDINGNAME, self.id)