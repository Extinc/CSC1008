import json

from django.db.models import Q
from django.utils import timezone

from LIFT.codes.BookingFunctions import haversine
# from LIFT.codes.Haversine import haversine
from LIFT.codes.Routes import roadnode_df, roadedge_df
from LIFT.datastructure.Graph import Graph
from LIFT.models.models import PathCache


class PathFinder:
    def __init__(self):
        self.graph = Graph()
        self.shortest_path = None

    # This function is used to build graph
    def find_path(self, startlat, startlong, endlat, endlong):
        self.graph = Graph()
        end = roadnode_df.loc[(roadnode_df['x'] == endlong) & (roadnode_df['y'] == endlat)]['id'].values[0]
        start = roadnode_df.loc[(roadnode_df['x'] == startlong) & (roadnode_df['y'] == startlat)]['id'].values[
            0]

        # If start and end location exist within the database get the stored graph
        if PathCache.objects.filter(Q(source=start) & Q(destination=end)).count() > 0:
            # Load the graph directly from database when it is stored already
            # This is to speed up processing to reduce the need of building the graph everytime.
            path_cache = PathCache.objects.get(source=start, destination=end)
            self.graph.adj_list = json.loads(path_cache.graph)
            self.graph.heuristic = json.loads(path_cache.heuristic)
        else:
            # Below is to build the graph
            next_node = []
            nodecounter = 0

            # Using haversine to calculate the distance for heuristic
            heuristic = haversine(startlong, startlat, endlong, endlat) * 1000

            # First add the starting node and heuristic to the graph
            self.graph.addNode(start)
            self.graph.addHeuristic(start, heuristic)

            # Filter and only keep edge that is connected to the starting node
            filtered = roadedge_df.loc[roadedge_df['source'] == start].values

            # add the edge connected to the starting node to the graph
            for node in filtered:
                templat = roadnode_df.loc[roadnode_df['id'] == node[1]]['y'].values[0]
                templong = roadnode_df.loc[roadnode_df['id'] == node[1]]['x'].values[0]
                heuristic = haversine(templong, templat, endlong, endlat)
                self.graph.addEdge(start, node[1], float(node[2]))
                self.graph.addHeuristic(node[1], heuristic)
                next_node.append(node[1])

            # Continuously add in nodes till it reach the end node.
            # TO build the graph where all possible edges are cnnected between the starting node and end node.
            while end not in next_node:
                filtered = roadedge_df.loc[roadedge_df['source'] == next_node[nodecounter]].values
                for node in filtered:
                    if node[1] not in next_node:
                        templat = roadnode_df.loc[roadnode_df['id'] == node[0]]['y'].values[0]
                        templong = roadnode_df.loc[roadnode_df['id'] == node[0]]['x'].values[0]
                        heuristic = haversine(templong, templat, endlong, endlat)
                        self.graph.addEdge(node[0], node[1], float(node[2]), heuristic)
                        self.graph.addHeuristic(node[0], heuristic)

                        templat = roadnode_df.loc[roadnode_df['id'] == node[1]]['y'].values[0]
                        templong = roadnode_df.loc[roadnode_df['id'] == node[1]]['x'].values[0]
                        heuristic = haversine(templong, templat, endlong, endlat)
                        self.graph.addHeuristic(node[1], heuristic)
                        next_node.append(node[1])
                nodecounter += 1

            # store the graph in the database
            # if exist update if do not exist create in database
            _, _ = PathCache.objects.update_or_create(source=start, destination=end,
                                                      defaults={'source': start, 'destination': end,
                                                                        'DateTime': timezone.now(),
                                                                        'graph': json.dumps(self.graph.adj_list),
                                                                        'heuristic': json.dumps(self.graph.heuristic)})
            del next_node
        self.shortest_path = self.graph.pathfind_astar(start, end)

    # Function to generate the geojson data for plotting the route
    def generate_geojson(self, type):
        geom = {'type': type, 'coordinates': []}
        for i in range(len(self.shortest_path) - 1):
            geom['coordinates'] = geom['coordinates'] + roadedge_df.loc[
                (roadedge_df['source'] == self.shortest_path[i]) & (roadedge_df['dest'] == self.shortest_path[i + 1])][
                'geometry'].values[0]
        return geom
