class Graph:
    def __init__(self):
        self.adj_list = {}  # This is used to store the adajacency list
        self.heuristic = {}  # This is to store heuristic data for the nodes

    # Function to get the neighbors of the node
    def get_neighbors(self, node):
        return self.adj_list[node]

    # Function to add node to the graph
    def addNode(self, node):
        self.adj_list[node] = []

    # FUnction to add heuristic data to the graph on creating the graph
    def addHeuristic(self, node, heu):
        self.heuristic[node] = heu

    # Funtion to add the edges to the graph
    def addEdge(self, src, dest, distance=0, heu=0):
        if src not in self.adj_list:
            self.addNode(src)
        if dest not in self.adj_list:
            self.addNode(dest)
        if (dest, distance) not in self.adj_list[src]:
            self.adj_list[src].append((dest, distance))

    # This is to get the heuristic
    def h(self, n):
        return self.heuristic[n]

    # A star path finding Algorithm to find the shortest_path within the graph
    def pathfind_astar(self, start, destination):
        # In this open_lst is a list of nodes which have been visited, but who's
        # neighbours haven't all been always visited, It start with the starting node
        # And closed_lst is a list of nodes which have been visited
        # and who's neighbors have been always visited
        open_lst = {start}
        closed_lst = set([])

        # distance has present distances from start to all other nodes
        present_dist = {start: 0}

        # adjacent_map contains an adjacent maps of all nodes
        adjacent_map = {start: start}

        while len(open_lst) > 0:
            n = None

            # it will find a node with the lowest value of f() = g() + h() :
            for v in open_lst:
                if n is None or present_dist[v] + self.h(v) < present_dist[n] + self.h(n):
                    n = v

            if n is None:
                print('Path is not existent!')
                return None

            # if the current node is the stop
            # then we start again from start
            if n == destination:
                reconst_path = []

                while adjacent_map[n] != n:
                    reconst_path.append(n)
                    n = adjacent_map[n]

                reconst_path.append(start)

                reconst_path.reverse()

                print('Path found: {}'.format(reconst_path))
                # Path is found Return the shortest path found
                return reconst_path

            # for all the neighbors of the current node do the following
            for (m, distance) in self.get_neighbors(n):
                # if the current node is not present in both open_lst and closed_lst
                # add it to open_lst and note n as it's adjacent map
                if m not in open_lst and m not in closed_lst:
                    open_lst.add(m)
                    adjacent_map[m] = n
                    present_dist[m] = present_dist[n] + distance

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update the data
                # and if the node was in the closed_lst, move it to open_lst
                else:
                    if present_dist[m] > present_dist[n] + distance:
                        present_dist[m] = present_dist[n] + distance
                        adjacent_map[m] = n

                        if m in closed_lst:
                            closed_lst.remove(m)
                            open_lst.add(m)

            # remove n from the open_lst, and add it to closed_lst
            # because all of the open_lst neighbors has been visited
            open_lst.remove(n)
            closed_lst.add(n)

        print('Path is not existent!')
        return None
