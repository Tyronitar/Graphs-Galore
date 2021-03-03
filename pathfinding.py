from graph_tool.all import *
from graph_utils import dist
from queue import PriorityQueue
from math import sqrt, inf

def Dijkstra(g, pos_, start, end):
    dist_ = g.new_vertex_property("double")
    prev_ = g.new_vertex_property("object")
    path_vert_ = g.new_vertex_property("bool")
    path_edge_ = g.new_edge_property("bool")

    for e in g.edges():
        path_edge_[e] = False

    Q = PriorityQueue()

    for v in g.get_vertices():
        dist_[v] = inf
        prev_[v] = None
        path_vert_[v] = False
        Q.put((dist_[v], v))

    dist_[start] = 0
    Q.put((0, start))
    
    while not Q.empty():
        nxt = Q.get()
        u = nxt[1]

        if u == end:
            break

        for n in g.get_out_neighbors(u):
            alt = dist_[u] + dist(u, n, pos_)
            if alt < dist_[n]:
                dist_[n] = alt
                Q.put((alt, n))
                prev_[n] = u
    
    # recreate path
    u = end
    if prev_[u] != None or u == start:
        while u != None:
            path_vert_[u] = True
            if prev_[u] != None:
                e = g.edge(u, prev_[u])
                path_edge_[e] = True
            u = prev_[u]
    
    return (path_vert_, path_edge_)