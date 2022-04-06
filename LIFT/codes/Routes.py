import json

import pandas as pd
import random

from LIFT.codes.BookingFunctions import haversine
from django.contrib.auth.models import User, Group
from LIFT.models.models import PointInfo, Drivers, UserActivity
from LIFTMAIN.settings import DRIVE_EDGE_DATA, DRIVE_NODE_DATA

edge_data = []
node_data = []

"""
To Read the edge data and store it within pandas
"""
f = open(DRIVE_EDGE_DATA)
data = json.load(f)
for feature in data["features"]:
    if feature["properties"]["access"] != "no" or feature["properties"]["access"] == "no,permissive":
        edge_data.append({"source": feature["properties"]["source"], "dest": feature["properties"]["dest"],
                          "length": feature["properties"]["length"], "highway": feature["properties"]["highway"],
                          "geometry": feature["geometry"]["coordinates"]})
f.close()

"""
To Read all the node data and store it within pandas
"""
f = open(DRIVE_NODE_DATA)
data = json.load(f)
points = None
for feature in data["features"]:
    node_data.append({"id": feature["properties"]["id"], "highway": feature["properties"]["highway"],
                      "x": feature["properties"]["x"], "y": feature["properties"]["y"],
                      "geometry_type": feature["geometry"]["type"], "geometry": feature["geometry"]["coordinates"]})
f.close()

roadedge_df = pd.DataFrame(edge_data)
roadnode_df = pd.DataFrame(node_data)
points_df = pd.DataFrame(
    list(PointInfo.objects.exclude(BUILDINGNAME__isnull=True).exclude(BUILDINGNAME__exact='', POSTALCODE__exact='').values('id', 'BUILDINGNAME', 'BLOCK', 'ROAD', 'POSTALCODE', 'lat', 'long')))

def find_nearest(lat, long):
    distance = points_df.apply(lambda row: pd.Series({"distance": haversine(long, lat, row['long'], row['lat']) * 1000}), result_type='expand', axis= 1)
    df = pd.concat([points_df, distance], axis=1).sort_values(by='distance', ascending=True)
    df = df[df['POSTALCODE'].str.len() > 0]
    return df.head(5)


# print(PointInfo.objects.all()[counte].lat)
# lastname = []
# with open('/Users/voidky/Documents/SIT_MODULE/CSC1008/DSAProjApp/LIFT/codes/names.txt') as f:
#     lines = f.readlines()
#     for data in lines:
#         lastname.append(data.rstrip('\n'))
# middlename = []
# with open('/Users/voidky/Documents/SIT_MODULE/CSC1008/DSAProjApp/LIFT/codes/middlename.txt') as f:
#     lines = f.readlines()
#     for data in lines:
#         middlename.append(data.rstrip('\n'))
#
# letter1 = []
# letter2 = []
# with open('/Users/voidky/Documents/SIT_MODULE/CSC1008/DSAProjApp/LIFT/codes/letter.txt') as f:
#     lines = f.readlines()
#     for data in lines:
#         letter1.append(data.rstrip('\n'))
#         letter2.append(data.rstrip('\n'))

# namecounter = 0
# # for j in range(len(name)):
#   # print(random.choice(name))
# counter = 10
# # print(random.randint())
# seatchoi = [5,8]
# for i in range(PointInfo.objects.all().count()):
#     name = random.choice(middlename)+" " + random.choice(lastname)
#     rngint = random.randint(1000, 99999)
#     platenumber = 'S' + random.choice(letter1).upper() + random.choice(letter2).upper() + str(rngint) + random.choice(letter2).upper()
#     test = Drivers.objects.create(driverID=counter, name=name, driverlat=PointInfo.objects.all()[i].lat,
#                                   driverlong=PointInfo.objects.all()[i].long, seatNo=random.choice(seatchoi), status="online", carplate= platenumber)
#     test.save()
#     counter += 1
# usernamecount = 0
# for i in range(PointInfo.objects.all().count()):
#     customergrp = Group.objects.get(name='customer')
#     username = "testuser" + str(usernamecount)
#     email = username + "@email.com"
#     password = "test1234"
#     if not User.objects.filter(username=username):
#         user = User.objects.create_user(username=username, email=email, password=password)
#         user.first_name = random.choice(middlename)
#         user.last_name = random.choice(lastname)
#         user.save()
#         user.groups.add(customergrp)
#         obj = User.objects.get(username=username)
#         act = UserActivity.objects.create(user = obj, lat =PointInfo.objects.all()[i].lat, long=PointInfo.objects.all()[i].long)
#         act.save()
#     usernamecount += 1
"""_summary_
    Below to to delete the array that is temp used to store the the data
"""
del edge_data
del node_data
