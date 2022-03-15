import sys

class VertexOld:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}


    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

#
# class GraphOld:
#     def __init__(self):
#         self.vert_dict = {}
#         self.num_vertices = 0
#
#     def __iter__(self):
#         return iter(self.vert_dict.values())
#
#     def add_vertex(self, node):
#         self.num_vertices = self.num_vertices + 1
#         new_vertex = Vertex(node)
#         self.vert_dict[node] = new_vertex
#         return new_vertex
#
#     def get_vertex(self, n):
#         if n in self.vert_dict:
#             return self.vert_dict[n]
#         else:
#             return None
#
#     def add_edge(self, frm, to, cost=0):
#         if frm not in self.vert_dict:
#             self.add_vertex(frm)
#         if to not in self.vert_dict:
#             self.add_vertex(to)
#
#         self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
#         self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)
#
#     def get_vertices(self):
#         return self.vert_dict.keys()
#
#     def set_previous(self, current):
#         self.previous = current
#
#     def get_previous(self, current):
#         return self.previous

def shortest(v, path):
    # ''' make shortest path from v.previous'''
    if v.previous:
        path.append(v.previous.get_id())
        shortest(v.previous, path)
    return


class Graph:
    def __init__(self):
        self.data = {}

    def  printGraph(self):
        print(self.data)

    def addNode(self, node):
        self.data[node] = {}

    def addEdge(self, src, dest, distance=0):
        if src not in self.data:
            self.data[src] = {}
        if dest not in self.data:
            self.data[dest] = {}

        self.data[src][dest] = distance
        self.data[dest][src] = distance

    def getNodes(self):
        return self.data.keys()

    def getEdges(self, node):
        return self.data[node]


def dijkstra(graph, src, dest):
    shortest_distance = {}  # records the cost to reach to • that node. Going LO be updated as we move along the graph
    track_predecessor = {}  # keep track of the path that has • Led us to this node
    unseenNodes = graph  # to iterate through the entire graph.
    infinity = sys.maxsize  # infinity can basically be considered a very Large number
    path = []  # going to trace our journey back to the source • node optimal route•
    for node in unseenNodes:
        shortest_distance[node] = infinity
    shortest_distance[src] = 0
    while unseenNodes:
        min_distance_node = None
        for node in unseenNodes:
            if min_distance_node is None:
                min_distance_node = node
            elif shortest_distance[node] < shortest_distance[min_distance_node]:
                min_distance_node = node
        path_options = graph[min_distance_node].items()
        for child, weight in path_options:
            if weight + shortest_distance[min_distance_node] < shortest_distance[child]:
                shortest_distance[child] = weight + shortest_distance[min_distance_node]
                track_predecessor[child] = min_distance_node
        unseenNodes.pop(min_distance_node)

    currNode = dest
    while currNode != src:
        try:
            path.insert(0, currNode)
            currNode = track_predecessor[currNode]
        except KeyError:
            print("Path is not reachable")
            break
    path.insert(0, src)

    if shortest_distance[dest] != infinity:
        print("Shortest distance is " + str(shortest_distance[dest]))
        print("Optimal path is " + str(path))
    return path
# def dijkstra(self, graph, source, destination):
#     inf = sys.maxsize # Define the infinite value of
#     D = {}  # Final distances dict
#     P = {}  # Previous
#     unseen_nodes = []
#     for node in graph.keys():
#         D[node] = -1  # Vertices are unreachable
#         P[node] = ""
#         unseen_nodes.append(node)
#     D[source] = 0  # The start vertex needs no move
#
#     return path