import json
import pandas as pd
edge_data = []
node_data = []
f = open('LIFTMAIN/Database/drive_edge.geojson')
data = json.load(f)
for feature in data["features"]:
    edge_data.append({"source": feature["properties"]["source"], "dest": feature["properties"]["dest"], "length": feature["properties"]["length"], "highway": feature["properties"]["highway"], "geometry": feature["geometry"]["coordinates"]})
f.close()

f = open('LIFTMAIN/Database/drive_node.geojson')
data = json.load(f)
for feature in data["features"]:
    node_data.append({"id": feature["properties"]["id"], "highway": feature["properties"]["highway"], "x": feature["properties"]["x"], "y": feature["properties"]["y"], "geometry_type": feature["geometry"]["type"], "geometry": feature["geometry"]["coordinates"]})
f.close()

roadedge_df = pd.DataFrame(edge_data)
roadnode_df = pd.DataFrame(node_data)
del edge_data
del node_data