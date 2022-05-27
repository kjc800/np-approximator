import networkx as nx
import numpy as np


# param: graph, starting point, list of homes
# return: cycle running repeated Dijkstras on all homes
def repeatedDijkstras(graph, start, homes):
    cycle = []

    # begin cycle from start point
    dijkstra = minPath(graph, start, homes)
    del dijkstra[1][-1]
    cycle.extend(dijkstra[1])
    lastEnd = dijkstra[0]
    homes.remove(dijkstra[0])

    while len(homes) > 0:
        dijkstra = minPath(graph, lastEnd, homes)
        del dijkstra[1][-1]
        cycle.extend(dijkstra[1])
        lastEnd = dijkstra[0]
        homes.remove(dijkstra[0])
    
    # end cycle at start point
    cycle.extend(nx.dijkstra_path(graph, lastEnd, start))

    return cycle

# param: graph, starting point, list of ending points
# return: tuple containing ending point and path of the shortest path from start
# tuple format: (ending point, path from start to endpoint)
def minPath(graph, start, points):
    pathsDict = {}
    for point in points:
        pathsDict[point] = nx.dijkstra_path_length(graph, start, point)
    minPoint = min(pathsDict, key=pathsDict.get)
    return (minPoint, nx.dijkstra_path(graph, start, minPoint))
