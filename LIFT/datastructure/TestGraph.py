import json
import sys


class Graph:
    def __init__(self):
        self.data = {}

    def printGraph(self):
        print(self.data)

    def addNode(self, node):
        self.data[node] = {}

    def addEdge(self, src, dest, distance=0):
        if src not in self.data:
            self.data[src] = {}
        if dest not in self.data:
            self.data[dest] = {}

        self.data[src][dest] = distance
        # self.data[dest][src] = distance

    def getNodes(self):
        return self.data.keys()

    def getEdges(self, node):
        return self.data[node]

    def initGraph(self, datalist):
        # To initialize the graph with json data
        self.data = json.loads(datalist)


def dijkstra(graph, src, dest):
    shortest_distance = {}  # records the cost to reach to that node. Going LO be updated as we move along the graph
    predecessor = {}  # keep track of the path that have lead to this node
    unseen_nodes = graph  # to iterate through the entire graph.
    inf = sys.maxsize  # infinity can basically be considered a very Large number
    shortest_path = []  # going to trace our journey back to the source • node optimal route•
    for node in unseen_nodes:
        shortest_distance[node] = inf
    shortest_distance[src] = 0
    while unseen_nodes:
        min_distance_node = None
        for node in unseen_nodes:
            if min_distance_node is None:
                min_distance_node = node
            elif shortest_distance[node] < shortest_distance[min_distance_node]:
                min_distance_node = node
        path_options = graph[min_distance_node].items()
        for child, weight in path_options:
            if weight + shortest_distance[min_distance_node] < shortest_distance[child]:
                shortest_distance[child] = weight + shortest_distance[min_distance_node]
                predecessor[child] = min_distance_node
        unseen_nodes.pop(min_distance_node)

    currNode = dest
    while currNode != src:
        try:
            shortest_path.insert(0, currNode)
            currNode = predecessor[currNode]
        except KeyError:
            print("Path is not reachable")
            break
    shortest_path.insert(0, src)

    if shortest_distance[dest] != inf:
        print("Shortest distance is " + str(shortest_distance[dest]))
        print("Optimal path is " + str(shortest_path))
    return shortest_path
