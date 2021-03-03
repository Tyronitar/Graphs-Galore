from graph_tool.all import *
from math import sqrt, inf
from queue import PriorityQueue
from itertools import chain, combinations

def dist(v1, v2, pos_):
    v1_pos = pos_[v1]
    v2_pos = pos_[v2]
    return sqrt((v2_pos[0] - v1_pos[0])**2 + (v2_pos[1] - v1_pos[1])**2)

def edge_distances(g, pos_):
    dist_ = g.new_edge_property("double")
    for e in g.get_edges():
        source = e.source()
        target = e.target()
        dist_[e] = dist(source, target, pos_)
    return dist_

def distance_matrix_pos(g, pos_):
    D = {}
    for v1 in g.get_vertices():
        D[v1] = {}
        for v2 in g.get_vertices():
            if v1 == v2:
                D[v1][v2] = 0
            elif v2 in g.get_out_neighbors(v1):
                D[v1][v2] = dist(v1, v2, pos_)
            else:
                D[v1][v2] = inf
    return D

def distance_matrix_weights(g, weights):
    D = {}
    for v1 in g.vertices():
        D[v1] = {}
        for v2 in g.vertices():
            if v1 == v2:
                D[v1][v2] = 0
            else:
                D[v1][v2] = inf

    for e in g.get_edges([weights]):
        source = g.vertex(e[0])
        target = g.vertex(e[1])
        D[source][target] = e[2]
        if not g.is_directed():
            D[target][source] = e[2]

    return D

# def powerset(S):
#     x = len(S)
#     subsets = []
#     for i in range (2, 1 << x):
#         subsets.append(set([S[j] for j in range(x) if (i & (1 << j))]))
#     return subsets


def powerset(iterable, min_size=0):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(min_size, len(s)+1))

def highlight_path(g, path,v_color="#ff0000",e_color="#000000",path_color="#0000ff"):
    v_color_ = g.new_vertex_property("string")
    e_color_ = g.new_edge_property("string")
    for v in g.vertices():
        v_color_[v] = v_color
    for e in g.edges():
        e_color_[e] = e_color
    for i, v_id in enumerate(path):
        curr_v = g.vertex(v_id)
        v_color_[curr_v] = path_color
        if i < len(path) - 1:
            next_v = g.vertex(path[i + 1])
            e = g.edge(curr_v, next_v)
            e_color_[e] = path_color
    return (v_color_, e_color_)


#
# Four Color Theorem Stuff
#
possible_colors = ["#ff0000", "#00ff00", "#0000ff", "#eeff00", "#ff00ff", "#00ffff", "#ff8000"]
#                   red,      green,      blue,      yellow,    magenta,   cyan,      orange

def get_neighbor_colors(g, v, color_):
    color_set = set([])
    for n in g.get_all_neighbors(v):
        if not color_[n] == None:
            color_set.add(color_[n])
    return color_set

def sort_by_degree(g, reverse =True):
    vertices = []
    for v in g.get_vertices():
        vert = g.vertex(v)
        degree = vert.in_degree() + vert.out_degree()
        vertices.append((v, degree))
    vertices.sort(key=lambda x: x[1], reverse=reverse)
    vertices = [x[0] for x in vertices]
    return vertices

def sort_by_degree_list(g, ls, reverse =True):
    vertices = []
    for v in ls:
        vert = g.vertex(v)
        degree = vert.in_degree() + vert.out_degree()
        vertices.append((v, degree))
    vertices.sort(key=lambda x: x[1], reverse=reverse)
    vertices = [x[0] for x in vertices]
    return vertices

def common_neighbors(g, v1, v2):
    v1_neighbors = g.get_all_neighbors(v1)
    v2_neighbors = g.get_all_neighbors(v2)
    # cn = [v for v in v1_neighbors if v in v2_neighbors]
    cn = list(set(v1_neighbors) & set(v2_neighbors))
    return cn

def degree(g, v):
    vert = g.vertex(v)
    degree = vert.in_degree() + vert.out_degree()
    return degree

def find_highest_degree(g):
    max_degree = -1
    best = None
    for v in g.get_vertices():
        d = degree(g, v)
        if d > max_degree:
            max_degree = d
            best = v
    return best

def find_highest_degree_list(g, ls):
    max_degree = -1
    best = None
    for v in ls:
        d = degree(g, v)
        if d > max_degree:
            max_degree = d
            best = v
    return best


def contract_into(g, y, x):
    for n in g.get_all_neighbors(y):
        if n not in g.get_all_neighbors(x) and not n == x:
            # print(f"before adding edge to '{n}: {g.get_all_neighbors(x)}")
            g.add_edge(x, n)
            # print(f"after adding: {g.get_all_neighbors(x)}")

def contract_into2(g, y, x, NN):
    for n in g.get_all_neighbors(y):
        if n not in g.get_all_neighbors(x) and not n == x:
            # print(f"before adding edge to '{n}: {g.get_all_neighbors(x)}")
            g.add_edge(x, n)
            NN.remove(n)
            # print(f"after adding: {g.get_all_neighbors(x)}")
    NN.remove(y)





if __name__ == "__main__":
    pass