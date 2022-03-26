import json
from time import sleep

import pandas as pd
import requests

from LIFT.models.models import PointInfo, Drivers
from LIFTMAIN.settings import DRIVE_EDGE_DATA, DRIVE_NODE_DATA, ONEMAP_DEV_URL, ONEMAP_TOKEN


edge_data = []
node_data = []

"""
To Read the edge data and store it within pandas
"""
f = open(DRIVE_EDGE_DATA)
data = json.load(f)
for feature in data["features"]:
    if feature["properties"]["access"] != "no" or feature["properties"]["access"] == "no,permissive":
        edge_data.append({"source": feature["properties"]["source"], "dest": feature["properties"]["dest"], "length": feature["properties"]["length"], "highway": feature["properties"]["highway"], "geometry": feature["geometry"]["coordinates"]})
f.close()

"""
To Read all the node data and store it within pandas
"""
f = open(DRIVE_NODE_DATA)
data = json.load(f)
points = None
for feature in data["features"]:
    node_data.append({"id": feature["properties"]["id"], "highway": feature["properties"]["highway"], "x": feature["properties"]["x"], "y": feature["properties"]["y"], "geometry_type": feature["geometry"]["type"], "geometry": feature["geometry"]["coordinates"]})
f.close()


roadedge_df = pd.DataFrame(edge_data)
roadnode_df = pd.DataFrame(node_data)
points_df = pd.DataFrame(list(PointInfo.objects.all().values('id', 'BUILDINGNAME', 'BLOCK', 'ROAD', 'POSTALCODE', 'lat', 'long')))

print(points_df)
counte = 0

"""_summary_
    Below to to delete the array that is temp used to store the the data
"""
del edge_data
del node_data