from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from LIFTMAIN.settings import MAPBOX_PUBLIC_KEY
from ..codes.Routes import roadedge_df,roadnode_df
from ..datastructure.Graph import Graph, dijkstra


# Create your views here.
def landing_page(request):
    return render(request, 'landing.html')


@login_required(login_url='/login')
def index(request):
    args = {'title': "Home"}
    if request.user.is_authenticated:
        print(roadedge_df)
        args['mapbox_key'] = MAPBOX_PUBLIC_KEY
        fname = request.user.first_name
        args['fname'] = fname
        return render(request, 'index.html', args)
    else:
        return render(request, 'index.html', args)


# Jquery post Request Handling
def plot_route(request):
    if request.method == 'POST':
        graph = Graph()
        endcoord = [1.4410467, 103.839182]
        startcoord = [1.4180309, 103.8386927]
        end = roadnode_df.loc[(roadnode_df['x'] == endcoord[1]) & (roadnode_df['y'] == endcoord[0])]['id'].values[0]
        start = roadnode_df.loc[(roadnode_df['x'] == startcoord[1]) & (roadnode_df['y'] == startcoord[0])]['id'].values[
            0]

        next_node = []
        nodecounter = 0
        graph.addNode(start)

        filtered = roadedge_df.loc[roadedge_df['source'] == start].values
        for node in filtered:
            graph.addEdge(start, node[1], float(node[2]))
            next_node.append(node[1])

        while end not in next_node:
            filtered = roadedge_df.loc[roadedge_df['source'] == next_node[nodecounter]].values
            for next in filtered:
                if next[1] not in next_node:
                    graph.addEdge(next[0], next[1], float(next[2]))
                    next_node.append(next[1])
            nodecounter += 1

        shortest_path = dijkstra(graph.data, start, end)

        geom = {'type': 'LineString', 'coordinates': []}

        for i in range(len(shortest_path) - 1):
            geom['coordinates'] = geom['coordinates'] + roadedge_df.loc[
                (roadedge_df['source'] == shortest_path[i]) & (roadedge_df['dest'] == shortest_path[i + 1])][
                'geometry'].values[0]
            # print(geom['coordinates'])
        return JsonResponse(geom, safe=False)
