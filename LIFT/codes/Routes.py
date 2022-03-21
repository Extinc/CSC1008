import json
from time import sleep

import pandas as pd
import requests

from LIFT.models.models import PointInfo
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
points_df = pd.DataFrame(list(PointInfo.objects.all().values('id', 'BUILDINGNAME', 'BLOCK', 'ROAD', 'POSTALCODE')))

print(points_df)

# totalcount = 0
# count=0
# result = []

# dat = PointInfo.objects.all().filter(POSTALCODE__exact='NIL')
# dat = list(dat)
# print(dat)
# count = 0
# for i in dat:
#     print()
#     urls = "https://nominatim.openstreetmap.org/lookup?osm_ids=N" + str(i.id) + "&format=json"
#     response = requests.get(urls)
#     data1 = response.json()
#     if len(data1) > 0:
#         print(str(i.id) + str(data1))
#         PointInfo.objects.filter(id = i.id).update(POSTALCODE = data1[0]["address"]["postcode"])
#         PointInfo.objects.filter(id = i.id).update(ROAD = data1[0]["address"]["road"])
#     count += 1
#     print(count)
    # sleep(1.3)


"""_summary_
    Below to to delete the array that is temp used to store the the data
"""
del edge_data
del node_data