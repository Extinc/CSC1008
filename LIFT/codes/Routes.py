import json

import pandas as pd
from LIFT.codes.BookingFunctions import haversine
from LIFT.models.models import PointInfo
from LIFTMAIN.settings import DRIVE_EDGE_DATA, DRIVE_NODE_DATA

edge_data = []
node_data = []

"""
To Read the edge data
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
To Read all the node data
"""
f = open(DRIVE_NODE_DATA)
data = json.load(f)
points = None
for feature in data["features"]:
    node_data.append({"id": feature["properties"]["id"], "highway": feature["properties"]["highway"],
                      "x": feature["properties"]["x"], "y": feature["properties"]["y"],
                      "geometry_type": feature["geometry"]["type"], "geometry": feature["geometry"]["coordinates"]})
f.close()

'''
Store node & edge into pandas dataframe
'''
roadedge_df = pd.DataFrame(edge_data)
roadnode_df = pd.DataFrame(node_data)
points_df = pd.DataFrame(
    list(PointInfo.objects.exclude(BUILDINGNAME__isnull=True).exclude(BUILDINGNAME__exact='', POSTALCODE__exact='').values('id', 'BUILDINGNAME', 'BLOCK', 'ROAD', 'POSTALCODE', 'lat', 'long')))

def find_nearest(lat, long):
    distance = points_df.apply(lambda row: pd.Series({"distance": haversine(long, lat, row['long'], row['lat']) * 1000}), result_type='expand', axis= 1)
    df = pd.concat([points_df, distance], axis=1).sort_values(by='distance', ascending=True)
    df = df[df['POSTALCODE'].str.len() > 0]
    return df.head(5)

"""_summary_
    Below to to delete the array that is temp used to store the the data
"""
del edge_data
del node_data
