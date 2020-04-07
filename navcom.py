#!/usr/bin/env python3
"""
Hyperspace Navigation Computer
Calculate the distance between any two points in a chart by their connections
For reference
From: https://www.bogotobogo.com/python/python_Dijkstras_Shortest_Path_Algorithm.php
"""

import sys
from functools import total_ordering

@total_ordering
class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        # Set distance to infinity for all nodes
        self.distance = sys.maxsize
        # Mark all nodes unvisited
        self.visited = False
        # Predecessor
        self.previous = None

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

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.distance == other.distance
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.distance < other.distance
        return NotImplemented

    def __hash__(self):
        return id(self)

class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost = 0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous

def shortest(v, path):
    ''' make shortest path from v.previous'''
    if v.previous:
        path.append(v.previous.get_id())
        shortest(v.previous, path)
    return

import heapq

def dijkstra(aGraph, start, target):
    global route1x
    # Set the distance for the start node to zero
    start.set_distance(0)

    # Put tuple pair into the priority queue
    unvisited_queue = [(v.get_distance(),v) for v in aGraph]
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        # Pops a vertex with the smallest distance
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()

        #for next in v.adjacent:
        for next in current.adjacent:
            # if visited, skip
            if next.visited:
                continue
            new_dist = current.get_distance() + current.get_weight(next)

            if new_dist < next.get_distance():
                next.set_distance(new_dist)
                next.set_previous(current)
                # print('%s next = %s new_dist = %s' \
                #         %(current.get_id(), next.get_id(), next.get_distance()))
                # print(next.get_distance())

            # else:
            #     print('not updated : current = %s next = %s new_dist = %s' \
            #             %(current.get_id(), next.get_id(), next.get_distance()))

        # Rebuild heap
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Put all vertices not visited into the queue
        unvisited_queue = [(v.get_distance(),v) for v in aGraph if not v.visited]
        heapq.heapify(unvisited_queue)


if __name__ == '__main__':

    g = Graph()

    # List of Planets
    g.add_vertex('Allusol')
    g.add_vertex('Breshos')
    g.add_vertex('Broc')
    g.add_vertex('Cantac')
    g.add_vertex('Fala')
    g.add_vertex('Fin')
    g.add_vertex('Foisso')
    g.add_vertex('Gonu')
    g.add_vertex('Gustuc')
    g.add_vertex('Higoh')
    g.add_vertex('Jotha')
    g.add_vertex('Lidamuuh')
    g.add_vertex('Ligebur')
    g.add_vertex('Lond')
    g.add_vertex('Mund')
    g.add_vertex('Nieth')
    g.add_vertex('Peospa')
    g.add_vertex('Scon')
    g.add_vertex('Shube')
    g.add_vertex('Tathath')
    g.add_vertex('Truukar')
    g.add_vertex('Unte')
    g.add_vertex('Vas')
    g.add_vertex('Woiloth')
    g.add_vertex('Yeoth')

    g.add_edge('Allusol', 'Cantac', 46)
    g.add_edge('Allusol', 'Fala', 34)
    g.add_edge('Allusol', 'Scon', 36)
    g.add_edge('Allusol', 'Tathath', 11)
    g.add_edge('Breshos', 'Fin', 56)
    g.add_edge('Breshos', 'Gonu', 40)
    g.add_edge('Breshos', 'Lond', 38)
    g.add_edge('Broc', 'Yeoth', 43)
    g.add_edge('Cantac', 'Gonu', 43)
    g.add_edge('Cantac', 'Vas', 48)
    g.add_edge('Fala', 'Vas', 33)
    g.add_edge('Fin', 'Gustuc', 48)
    g.add_edge('Fin', 'Woiloth', 29)
    g.add_edge('Fin', 'Yeoth', 80)
    g.add_edge('Foisso', 'Gustuc', 24)
    g.add_edge('Foisso', 'Higoh', 20)
    g.add_edge('Gustuc', 'Truukar', 43)
    g.add_edge('Jotha', 'Mund', 14)
    g.add_edge('Jotha', 'Truukar', 28)
    g.add_edge('Lidamuuh', 'Tathath', 22)
    g.add_edge('Ligebur', 'Truukar', 21)
    g.add_edge('Ligebur', 'Yeoth', 92)
    g.add_edge('Lond', 'Peospa', 67)
    g.add_edge('Lond', 'Shube', 70)
    g.add_edge('Mund', 'Truukar', 21)
    g.add_edge('Nieth', 'Truukar', 34)
    g.add_edge('Nieth', 'Unte', 49)
    g.add_edge('Peospa', 'Shube', 28)
    g.add_edge('Scon', 'Woiloth', 18)
    g.add_edge('Shube', 'Vas', 56)
    g.add_edge('Tathath', 'Ryloth', 90)

    # print('Graph data:')
    # for v in g:
    #     for w in v.get_connections():
    #         vid = v.get_id()
    #         wid = w.get_id()
    #         print('( %s , %s, %3d)'  % ( vid, wid, v.get_weight(w)))

    ErtuSectorAllCombinations = [('Allusol', 'Breshos'), ('Allusol', 'Broc'), ('Allusol', 'Cantac'), ('Allusol', 'Fala'), ('Allusol', 'Fin'), ('Allusol', 'Foisso'), ('Allusol', 'Gonu'), ('Allusol', 'Gustuc'), ('Allusol', 'Higoh'), ('Allusol', 'Jotha'), ('Allusol', 'Lidamuuh'), ('Allusol', 'Ligebur'), ('Allusol', 'Lond'), ('Allusol', 'Mund'), ('Allusol', 'Nieth'), ('Allusol', 'Peospa'), ('Allusol', 'Scon'), ('Allusol', 'Shube'), ('Allusol', 'Tathath'), ('Allusol', 'Truukar'), ('Allusol', 'Unte'), ('Allusol', 'Vas'), ('Allusol', 'Woiloth'), ('Allusol', 'Yeoth'), ('Breshos', 'Broc'), ('Breshos', 'Cantac'), ('Breshos', 'Fala'), ('Breshos', 'Fin'), ('Breshos', 'Foisso'), ('Breshos', 'Gonu'), ('Breshos', 'Gustuc'), ('Breshos', 'Higoh'), ('Breshos', 'Jotha'), ('Breshos', 'Lidamuuh'), ('Breshos', 'Ligebur'), ('Breshos', 'Lond'), ('Breshos', 'Mund'), ('Breshos', 'Nieth'), ('Breshos', 'Peospa'), ('Breshos', 'Scon'), ('Breshos', 'Shube'), ('Breshos', 'Tathath'), ('Breshos', 'Truukar'), ('Breshos', 'Unte'), ('Breshos', 'Vas'), ('Breshos', 'Woiloth'), ('Breshos', 'Yeoth'), ('Broc', 'Cantac'), ('Broc', 'Fala'), ('Broc', 'Fin'), ('Broc', 'Foisso'), ('Broc', 'Gonu'), ('Broc', 'Gustuc'), ('Broc', 'Higoh'), ('Broc', 'Jotha'), ('Broc', 'Lidamuuh'), ('Broc', 'Ligebur'), ('Broc', 'Lond'), ('Broc', 'Mund'), ('Broc', 'Nieth'), ('Broc', 'Peospa'), ('Broc', 'Scon'), ('Broc', 'Shube'), ('Broc', 'Tathath'), ('Broc', 'Truukar'), ('Broc', 'Unte'), ('Broc', 'Vas'), ('Broc', 'Woiloth'), ('Broc', 'Yeoth'), ('Cantac', 'Fala'), ('Cantac', 'Fin'), ('Cantac', 'Foisso'), ('Cantac', 'Gonu'), ('Cantac', 'Gustuc'), ('Cantac', 'Higoh'), ('Cantac', 'Jotha'), ('Cantac', 'Lidamuuh'), ('Cantac', 'Ligebur'), ('Cantac', 'Lond'), ('Cantac', 'Mund'), ('Cantac', 'Nieth'), ('Cantac', 'Peospa'), ('Cantac', 'Scon'), ('Cantac', 'Shube'), ('Cantac', 'Tathath'), ('Cantac', 'Truukar'), ('Cantac', 'Unte'), ('Cantac', 'Vas'), ('Cantac', 'Woiloth'), ('Cantac', 'Yeoth'), ('Fala', 'Fin'), ('Fala', 'Foisso'), ('Fala', 'Gonu'), ('Fala', 'Gustuc'), ('Fala', 'Higoh'), ('Fala', 'Jotha'), ('Fala', 'Lidamuuh'), ('Fala', 'Ligebur'), ('Fala', 'Lond'), ('Fala', 'Mund'), ('Fala', 'Nieth'), ('Fala', 'Peospa'), ('Fala', 'Scon'), ('Fala', 'Shube'), ('Fala', 'Tathath'), ('Fala', 'Truukar'), ('Fala', 'Unte'), ('Fala', 'Vas'), ('Fala', 'Woiloth'), ('Fala', 'Yeoth'), ('Fin', 'Foisso'), ('Fin', 'Gonu'), ('Fin', 'Gustuc'), ('Fin', 'Higoh'), ('Fin', 'Jotha'), ('Fin', 'Lidamuuh'), ('Fin', 'Ligebur'), ('Fin', 'Lond'), ('Fin', 'Mund'), ('Fin', 'Nieth'), ('Fin', 'Peospa'), ('Fin', 'Scon'), ('Fin', 'Shube'), ('Fin', 'Tathath'), ('Fin', 'Truukar'), ('Fin', 'Unte'), ('Fin', 'Vas'), ('Fin', 'Woiloth'), ('Fin', 'Yeoth'), ('Foisso', 'Gonu'), ('Foisso', 'Gustuc'), ('Foisso', 'Higoh'), ('Foisso', 'Jotha'), ('Foisso', 'Lidamuuh'), ('Foisso', 'Ligebur'), ('Foisso', 'Lond'), ('Foisso', 'Mund'), ('Foisso', 'Nieth'), ('Foisso', 'Peospa'), ('Foisso', 'Scon'), ('Foisso', 'Shube'), ('Foisso', 'Tathath'), ('Foisso', 'Truukar'), ('Foisso', 'Unte'), ('Foisso', 'Vas'), ('Foisso', 'Woiloth'), ('Foisso', 'Yeoth'), ('Gonu', 'Gustuc'), ('Gonu', 'Higoh'), ('Gonu', 'Jotha'), ('Gonu', 'Lidamuuh'), ('Gonu', 'Ligebur'), ('Gonu', 'Lond'), ('Gonu', 'Mund'), ('Gonu', 'Nieth'), ('Gonu', 'Peospa'), ('Gonu', 'Scon'), ('Gonu', 'Shube'), ('Gonu', 'Tathath'), ('Gonu', 'Truukar'), ('Gonu', 'Unte'), ('Gonu', 'Vas'), ('Gonu', 'Woiloth'), ('Gonu', 'Yeoth'), ('Gustuc', 'Higoh'), ('Gustuc', 'Jotha'), ('Gustuc', 'Lidamuuh'), ('Gustuc', 'Ligebur'), ('Gustuc', 'Lond'), ('Gustuc', 'Mund'), ('Gustuc', 'Nieth'), ('Gustuc', 'Peospa'), ('Gustuc', 'Scon'), ('Gustuc', 'Shube'), ('Gustuc', 'Tathath'), ('Gustuc', 'Truukar'), ('Gustuc', 'Unte'), ('Gustuc', 'Vas'), ('Gustuc', 'Woiloth'), ('Gustuc', 'Yeoth'), ('Higoh', 'Jotha'), ('Higoh', 'Lidamuuh'), ('Higoh', 'Ligebur'), ('Higoh', 'Lond'), ('Higoh', 'Mund'), ('Higoh', 'Nieth'), ('Higoh', 'Peospa'), ('Higoh', 'Scon'), ('Higoh', 'Shube'), ('Higoh', 'Tathath'), ('Higoh', 'Truukar'), ('Higoh', 'Unte'), ('Higoh', 'Vas'), ('Higoh', 'Woiloth'), ('Higoh', 'Yeoth'), ('Jotha', 'Lidamuuh'), ('Jotha', 'Ligebur'), ('Jotha', 'Lond'), ('Jotha', 'Mund'), ('Jotha', 'Nieth'), ('Jotha', 'Peospa'), ('Jotha', 'Scon'), ('Jotha', 'Shube'), ('Jotha', 'Tathath'), ('Jotha', 'Truukar'), ('Jotha', 'Unte'), ('Jotha', 'Vas'), ('Jotha', 'Woiloth'), ('Jotha', 'Yeoth'), ('Lidamuuh', 'Ligebur'), ('Lidamuuh', 'Lond'), ('Lidamuuh', 'Mund'), ('Lidamuuh', 'Nieth'), ('Lidamuuh', 'Peospa'), ('Lidamuuh', 'Scon'), ('Lidamuuh', 'Shube'), ('Lidamuuh', 'Tathath'), ('Lidamuuh', 'Truukar'), ('Lidamuuh', 'Unte'), ('Lidamuuh', 'Vas'), ('Lidamuuh', 'Woiloth'), ('Lidamuuh', 'Yeoth'), ('Ligebur', 'Lond'), ('Ligebur', 'Mund'), ('Ligebur', 'Nieth'), ('Ligebur', 'Peospa'), ('Ligebur', 'Scon'), ('Ligebur', 'Shube'), ('Ligebur', 'Tathath'), ('Ligebur', 'Truukar'), ('Ligebur', 'Unte'), ('Ligebur', 'Vas'), ('Ligebur', 'Woiloth'), ('Ligebur', 'Yeoth'), ('Lond', 'Mund'), ('Lond', 'Nieth'), ('Lond', 'Peospa'), ('Lond', 'Scon'), ('Lond', 'Shube'), ('Lond', 'Tathath'), ('Lond', 'Truukar'), ('Lond', 'Unte'), ('Lond', 'Vas'), ('Lond', 'Woiloth'), ('Lond', 'Yeoth'), ('Mund', 'Nieth'), ('Mund', 'Peospa'), ('Mund', 'Scon'), ('Mund', 'Shube'), ('Mund', 'Tathath'), ('Mund', 'Truukar'), ('Mund', 'Unte'), ('Mund', 'Vas'), ('Mund', 'Woiloth'), ('Mund', 'Yeoth'), ('Nieth', 'Peospa'), ('Nieth', 'Scon'), ('Nieth', 'Shube'), ('Nieth', 'Tathath'), ('Nieth', 'Truukar'), ('Nieth', 'Unte'), ('Nieth', 'Vas'), ('Nieth', 'Woiloth'), ('Nieth', 'Yeoth'), ('Peospa', 'Scon'), ('Peospa', 'Shube'), ('Peospa', 'Tathath'), ('Peospa', 'Truukar'), ('Peospa', 'Unte'), ('Peospa', 'Vas'), ('Peospa', 'Woiloth'), ('Peospa', 'Yeoth'), ('Scon', 'Shube'), ('Scon', 'Tathath'), ('Scon', 'Truukar'), ('Scon', 'Unte'), ('Scon', 'Vas'), ('Scon', 'Woiloth'), ('Scon', 'Yeoth'), ('Shube', 'Tathath'), ('Shube', 'Truukar'), ('Shube', 'Unte'), ('Shube', 'Vas'), ('Shube', 'Woiloth'), ('Shube', 'Yeoth'), ('Tathath', 'Truukar'), ('Tathath', 'Unte'), ('Tathath', 'Vas'), ('Tathath', 'Woiloth'), ('Tathath', 'Yeoth'), ('Truukar', 'Unte'), ('Truukar', 'Vas'), ('Truukar', 'Woiloth'), ('Truukar', 'Yeoth'), ('Unte', 'Vas'), ('Unte', 'Woiloth'), ('Unte', 'Yeoth'), ('Vas', 'Woiloth'), ('Vas', 'Yeoth'), ('Woiloth', 'Yeoth')]

    a = sys.argv[1]
    b = sys.argv[2]
    dijkstra(g, g.get_vertex(a), g.get_vertex(b))

    target = g.get_vertex(b)
    path = [target.get_id()]
    shortest(target, path)
    shortie = path
    print('The shortest path : %s' %(path[::-1]))
    print(path[0] + " to " + path[-1] + " = " + str(g.vert_dict[b].get_distance()))


# >>> str(g.vert_dict['Allusol'])
# "Allusol adjacent: ['Cantac', 'Fala', 'Scon', 'Tathath']"

# >>> str(g.vert_dict['Allusol'].get_distance())
# '46'

# >>> str(g.vert_dict[shortie[-1]].get_distance())
# '57'
