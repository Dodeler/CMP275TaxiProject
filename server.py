import sys
from adjacencygraph import AdjacencyGraph

'''

    This program provides communication support between server and client, handling requests
    for paths of an AdjacencyGraph by determining the best routes.  As well as
    ensuring that the client acknowledges each waypoint of the determined route.

    The file 'server.py' is to be used in conjunction with the adjacencygraph class
    developed in class, and may be executed on its own for testing purposes.

    This code was developed by Delaney Lothian and Chris Dodic.
    Delaney developed Dijkstra's algorithm with some bug correction help from Chris.
    Chris developed the server/client interaction algorithm, as well as the
    closest_vertex search function.

    Minimal error handling exists for invalid requests; if the input is flagged
    as a request, and the correct number of fields is present
    (lat and lon for both vertices) then the request will proceed, otherwise no
    action will be taken. This is chosen to minimize erroneous output to the client.
    The closest_vertex search algorithm is quite simple and works by checking each node.
    In this case, the search performs acceptably fast. However, if the graph being
    searched was much larger, a more targeted approach should be utilized.

    Updated: March 1, 2017
    Chris Dodic (1515299) and Delaney Lothian (1441546)

'''


coordinates = {}
streetnames = {}
edge_weights = {}

def least_cost_path(graph, start, dest, cost):
    """
        Find and return a least cost path in graph from start
        vertex to dest vertex.
        Efficiency: If E is the number of edges, the run-time is
        O( E log(E) ).
    Args:
        graph (Graph): The digraph defining the edges between the
        vertices.
        start: The vertex where the path starts. It is assumed
        that start is a vertex of graph.
        dest: The vertex where the path ends. It is assumed
        that start is a vertex of graph.
    Cost:
        A function, taking the two vertices of an edge as
        parameters and returning the cost of the edge. For its
        interface, see the definition of cost_distance.
        Returns:
    List:
        A potentially empty list (if no path can be found) of
        the vertices in the graph. If there was a path, the first
        vertex is always start, the last is always dest in the list.
        Any two consecutive vertices correspond to some
        edge in graph.
    """

    inf = float('inf')
    #Set all inital distances to be infinity
    dist = {vertex: inf for vertex in graph.vertices()}
    #Create dictionary of vertices without previous
    previous = {vertex: None for vertex in graph.vertices()}
    dist[start] = 0
    #The working heap (our sorting method)
    Q = MinHeap()
    #Initializes the cost of the initial vertex
    Q.add(dist[start], start)
    #While heap is non-empty:
    while Q:
        # Removes vertex with least weight from heap
        v = Q.pop_min()[1]
        # Inspects neighbours of removed vertex
        for neighbour in graph.neighbours(v):
            #If the cost of the neighbour is greater than the sum of the cost
            #of the parent vertex and the cost of the distance between them
            if dist[neighbour] > dist[v] + cost(v,neighbour):
                #Set the cost of the neighbour to this sum
                dist[neighbour] = dist[v] + cost(v,neighbour)
                #Add this neighbour to the heap
                Q.add(dist[neighbour], neighbour)
                #Create directional pair
                previous[neighbour] = v
            else:
                continue
    path = list()
    #If no path was found, return empty list
    if previous[dest] == None:
        return path
    else:
        #otherwise follow directional pairs back to "start" and add to path
        path.append(dest)
        currentv = dest
        while currentv != start:
            path.append(previous[currentv])
            currentv = previous[currentv]
        path.reverse()
        return path


def read_city_graph(filename):
    """
    Args:
        filename (str): Name of file

    Returns:
        AdjacencyGraph: Graph representing the city of Edmonton Roads
    """
    g = AdjacencyGraph()
    with open(filename) as f:
        for line in f:
            #split line seperated by ','
            line = line.split(',')
            if line[0] == 'V':
                #if line starts with a V, add vertex
                g.add_vertex(int(line[1]))
                latitude  = int(float(line[2])*100000)
                longitude = int(float(line[3])*100000)
                coordinates[int(line[1])] = (latitude, longitude)
            elif line[0] == 'E':
                #if line starts with a E, add edge
                edge = (int(line[1]), int(line[2]))
                g.add_edge(edge)
                streetnames[edge] = line[3]
                edge_weights[edge] = cost_distance(edge[0], edge[1])
            else:
                print('Not an edge nor a vertex')
    return g


def cost_distance(u, v):
    """

    Calculates the Euclidean distance between two vertices

    Args:
        vertices u and v from associated graph

    Returns:
        cost value of the edge connecting u and v
    """
    coord_u = coordinates[u]
    coord_v = coordinates[v]
    x = abs(coord_u[1] - coord_v[1])
    y = abs(coord_u[0] - coord_v[0])
    return (x*x + y*y)**(1/2)


def closest_vertex(lat, lon):
    """

    Determines the closest vertex to the specified location (latitude, longitude)

    Args:
        latitude and longitude of requested location

    Returns:
        closest vertex to the requested location
    """


    minimum=float('inf')
    # For each vertex in the graph:
    for key in coordinates:
        #Calculate the change in position fro        m vertex to specified location
        x=(lat-coordinates[key][0])
        y=(lon-coordinates[key][1])
        x=(x*x)
        y=(y*y)
        dist=(x+y)**(1/2)
        # Determines the closest point by comparing to current minimum
        if dist < minimum:
            minimum = dist
            min_vertex=key
    return min_vertex



class MinHeap:

    def __init__(self):
        self._array = []

    def add(self, key, value):
        self._array.append((key, value))
        self.fix_heap_up(len(self._array)-1)

    def pop_min(self):
        if not self._array:
            raise RuntimeError("Attempt to call pop_min on empty heap")
        retval = self._array[0]
        self._array[0] = self._array[-1]
        del self._array[-1]
        if self._array:
            self.fix_heap_down(0)
        return retval

    def fix_heap_up(self, i):
        if self.isroot(i):
            return
        p = self.parent(i)
        if self._array[i][0] < self._array[p][0]:
            self.swap(i, p)
            self.fix_heap_up(p)

    def swap(self, i, j):
        self._array[i], self._array[j] = \
            self._array[j], self._array[i]

    def isroot(self, i):
        return i == 0

    def isleaf(self, i):
        return self.lchild(i) >= len(self._array)

    def lchild(self, i):
        return 2*i+1

    def rchild(self, i):
        return 2*i+2

    def parent(self, i):
        return (i-1)//2

    def min_child_index(self, i):
        l = self.lchild(i)
        r = self.rchild(i)
        retval = l
        if r < len(self._array) and self._array[r][0] < self._array[l][0]:
            retval = r
        return retval

    def isempty(self):
        return len(self._array) == 0

    def length(self):
        return len(self._array)

    def fix_heap_down(self, i):
        if self.isleaf(i):
            return

        j = self.min_child_index(i)
        if self._array[i][0] > self._array[j][0]:
            self.swap(i, j)
            self.fix_heap_down(j)

    # Some stnadard collection interfaces

    # So the len() function will work.
    def __len__(self):
        return len(self._array)

    # Iterator
    def __iter__(self):
        return iter(self._array)

    def __next__(self):
        return (self._array).__next__
