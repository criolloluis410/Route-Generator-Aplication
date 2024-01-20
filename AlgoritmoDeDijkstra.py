# Import necessary modules: sys to handle infinite values, and heappop, heappush from heapq to handle the priority queue.
import sys
from heapq import heappop, heappush

# Define the Node class, representing a node in the graph with an identifier (vertex) and an accumulated weight (weight) from the source node.
class Node:
    resultList = []  # Class list used to store formatted results for printing.
    resultList2 = []  # Class list used to store route and cost information for further analysis.

    def __init__(self, edges, n):
        # Initialize the graph's adjacency list using information from the provided edges.
        self.adjList = [[] for _ in range(n)]
        for (source, dest, weight) in edges:
            self.adjList[source].append((dest, weight))

    # The __lt__ method is defined to allow node comparison based on weight. Necessary for using Node objects in the priority queue.
    def __lt__(self, other):
        return self.weight < other.weight

# Define the GraphD class, representing the directed weighted graph.
class GraphD:
    def get_route(prev, i, route):
        # Function used to construct the route from the source node to a given node (i) using information stored in the prev array.
        if i >= 0:
            get_route(prev, prev[i], route)
            route.append(i)

    def findShortestPaths(graph, source, n):
        pq = []
        heappush(pq, Node(source))
        dist = [sys.maxsize] * n
        dist[source] = 0
        done = [False] * n
        done[source] = True
        prev = [-1] * n

        while pq:
            # Explore nodes in order of the smallest accumulated cost using a priority queue.
            node = heappop(pq)
            u = node.vertex 

            for (v, weight) in graph.adjList[u]:
                if not done[v] and (dist[u] + weight) < dist[v]:
                    # Update minimum costs and store route information using the get_route function.
                    dist[v] = dist[u] + weight
                    prev[v] = u
                    heappush(pq, Node(v, dist[v]))

            done[u] = True

        route = []
        for i in range(n):
            if i != source and dist[i] != sys.maxsize:
                get_route(prev, i, route)
                # Add route and cost information to the resultList and resultList2 lists.
                GraphD.resultList.append(f'Path ({source} —> {i}): Minimum cost = {dist[i]}, Route = {route}')
                path = list(route)
                GraphD.resultList2.append((source, i, dist[i], path))
                route.clear()
