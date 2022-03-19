import json
from time import sleep

import pandas as pd
import requests

from LIFT.models.models import PointInfo
from LIFTMAIN.settings import DRIVE_EDGE_DATA, DRIVE_NODE_DATA, ONEMAP_DEV_URL, ONEMAP_TOKEN

edge_data = []
node_data = []
f = open(DRIVE_EDGE_DATA)
data = json.load(f)
for feature in data["features"]:
    if feature["properties"]["access"] != "no" or feature["properties"]["access"] == "no,permissive":
        edge_data.append({"source": feature["properties"]["source"], "dest": feature["properties"]["dest"], "length": feature["properties"]["length"], "highway": feature["properties"]["highway"], "geometry": feature["geometry"]["coordinates"]})
f.close()

f = open(DRIVE_NODE_DATA)
data = json.load(f)
for feature in data["features"]:
    node_data.append({"id": feature["properties"]["id"], "highway": feature["properties"]["highway"], "x": feature["properties"]["x"], "y": feature["properties"]["y"], "geometry_type": feature["geometry"]["type"], "geometry": feature["geometry"]["coordinates"]})
f.close()

roadedge_df = pd.DataFrame(edge_data)
roadnode_df = pd.DataFrame(node_data)
totalcount = 0
count=0
result = []
# for index, data in roadnode_df.iterrows():
#     # print()
#     if not PointInfo.objects.filter(id=data["id"]).exists():
#         if count == 250:
#             result = []
#             sleep(20)
#             count = 0
#         urls = ONEMAP_DEV_URL+ "/privateapi/commonsvc/revgeocode"
#         params ={}
#         params["location"] = str(data['geometry'][1]) + "," +str(data['geometry'][0])
#         params["token"] = ONEMAP_TOKEN
#         params["buffer"] = 10
#         params["addressType"] = "All"
#         params["otherFeatures"] = "N"
#         response = requests.get(urls, params=params)
#         data1 = response.json()
#         # js = []
#         if "GeocodeInfo" in data1 and len(data1["GeocodeInfo"]) > 0:
#             # js = {"id": data["id"], "INFO": data1["GeocodeInfo"][0]}
#             info = data1["GeocodeInfo"][0]
#             buildingname = ""
#             block = ""
#             road = ""
#             postalcode = ""
#             featurename = ""
#             id = data["id"]
#             if 'BUILDINGNAME' in info:
#                 buildingname = info['BUILDINGNAME']
#             if "BLOCK" in info:
#                 block = info["BLOCK"]
#             if 'ROAD' in info:
#                 road = info['ROAD']
#             if "POSTALCODE" in info:
#                 postalcode = info["POSTALCODE"]
#             if "FEATURE_NAME" in info:
#                 featurename = info["FEATURE_NAME"]
#
#             obj, created = PointInfo.objects.get_or_create(
#                 id=id,
#                 BUILDINGNAME=buildingname,
#                 BLOCK=block,
#                 ROAD=road,
#                 FEATURENAME=featurename,
#                 POSTALCODE=postalcode,
#             )
#             # result.append(js)
#             # print(count)
#             count += 1
#
#         totalcount += 1
#         # print(data)
#         print("CHECKING : " + str(index))
#



del edge_data
del node_data