from graph_tool.all import *
from graph_utils import *
from time import time



def sequential_coloring(g):
    # attempts to color graph based on Welsh-Powell algorithm
    colors_used = set([])
    color_ = g.new_vertex_property("string")

    # If it doesn't work there will be black
    for v in g.get_vertices():
        color_[v] = "#eeff00"

    sorted_vertices = sort_by_degree(g)
    for v in sorted_vertices:
        adj_colors = get_neighbor_colors(g, v, color_)
        for c in possible_colors:
            if c not in adj_colors:
                color_[v] = c
                colors_used.add(c)
                break
    print(f"Colors used: {len(colors_used)}, {colors_used}")
    return color_

def RLF(g, name_):
    start = time()
    color_ = g.new_vertex_property("string")
    for v in g.get_vertices():
        color_[v] = "#000000"
    color_number = 0
    G = Graph(g, prune=True)
    sorted_vertices = sort_by_degree(G)
    while G.num_vertices() > 0:
        x = sorted_vertices.pop(0)
        color_number += 1
        color_[x] = possible_colors[color_number - 1]

        # NN = GraphView(G, vfilt= lambda v: v not in G.get_all_neighbors(x) and not v == x)
        NN = [v for v in G.get_vertices() if v not in G.get_all_neighbors(x) and not v == x]
        # print(f"\nx: {x}/{name_[x]}, NN: {len(NN)}, G: {G.num_vertices()}")
        while len(NN) > 0:
            # print(f"x: {x}, NN: {NN.num_vertices()}, G: {G.num_vertices()}")
            print(f"\nx: {x}/{name_[x]}, NN: {len(NN)}, G: {G.num_vertices()}")
            y = None
            maxcn = -1
            ydegree = -1
            for z in NN:
                cn = len(common_neighbors(G, x, z))
                if cn > maxcn or (cn == maxcn and degree(G, z) < ydegree):
                    y = z
                    ydegree = degree(G, y)
                    maxcn = cn
            if maxcn == 0:
                # y = sort_by_degree(NN)[0]
                y = sort_by_degree_list(G, NN)[0]
            color_[y] = possible_colors[color_number - 1]
            # print(f"y: {y}, name: {name_[y]}")

            # print(f"x neighbors before contracting: {G.get_all_neighbors(x)}")
            # print(f"non neighbors before contracting: {NN}")
            # print(f"G before contracting {y}: {G.get_vertices()}")
            contract_into(G, y, x)
            G = GraphView(G, vfilt= lambda v: not v == y)
            # print(f"G after contracting {y}: {G.get_vertices()}")
            # x = sort_by_degree(G)[0]
            # print(f"x neighbors after contracting: {G.get_all_neighbors(x)}")
            # NN = GraphView(G, vfilt= lambda v: v not in G.get_all_neighbors(x) and not v == x)
            NN = [v for v in G.get_vertices() if v not in G.get_all_neighbors(x) and not v == x]
        G = GraphView(G, vfilt= lambda v: not v == x)
        sorted_vertices = sort_by_degree(G)
    end = time()
    print(f"\nNumber of colors: {color_number}\nElapsed Time: {end - start}")
    return color_

def RLF2(g, name_):
    start = time()
    color_ = g.new_vertex_property("string")
    for v in g.get_vertices():
        color_[v] = "#000000"
    color_number = 0
    G = Graph(g, prune=True)
    while G.num_vertices() > 0:
        x = find_highest_degree(G)
        color_number += 1
        color_[x] = possible_colors[color_number - 1]

        # NN = GraphView(G, vfilt= lambda v: v not in G.get_all_neighbors(x) and not v == x)
        # NN = [v for v in G.get_vertices() if v not in G.get_all_neighbors(x) and not v == x]
        NN = list(set(G.get_vertices()) - (set(G.get_all_neighbors(x)) | set([x])))
        NN = sort_by_degree_list(G, NN, reverse=False)
        # print(f"\nx: {x}/{name_[x]}, NN: {len(NN)}, G: {G.num_vertices()}")
        while len(NN) > 0:
            # print(f"x: {x}, NN: {NN.num_vertices()}, G: {G.num_vertices()}")
            print(f"\nx: {x}/{name_[x]}, NN: {len(NN)}, G: {G.num_vertices()}")
            y = None
            maxcn = -1
            ydegree = -1
            for z in NN:
                cn = len(common_neighbors(G, x, z))
                if cn > maxcn or (cn == maxcn and degree(G, z) < ydegree):
                    y = z
                    ydegree = degree(G, y)
                    maxcn = cn
            if maxcn == 0:
                # y = sort_by_degree(NN)[0]
                # y = find_highest_degree_list(g, NN)
                y = NN[len(NN) - 1]
            color_[y] = possible_colors[color_number - 1]
            # print(f"y: {y}, name: {name_[y]}")

            # print(f"x neighbors before contracting: {G.get_all_neighbors(x)}")
            # print(f"non neighbors before contracting: {NN}")
            # print(f"G before contracting {y}: {G.get_vertices()}")
            contract_into2(G, y, x,NN)
            G = GraphView(G, vfilt= lambda v: not v == y)
            # print(f"G after contracting {y}: {G.get_vertices()}")
            # x = sort_by_degree(G)[0]
            # print(f"x neighbors after contracting: {G.get_all_neighbors(x)}")
            # NN = GraphView(G, vfilt= lambda v: v not in G.get_all_neighbors(x) and not v == x)
        G = GraphView(G, vfilt= lambda v: not v == x)
    end = time()
    print(f"\nNumber of colors: {color_number}\nElapsed Time: {end - start}")
    return color_