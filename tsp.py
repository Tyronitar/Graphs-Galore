from graph_tool.all import *
from graph_utils import *
from math import inf



def held_karp(g, D, start):
    G = Graph(g, prune=True)
    cost = dict.fromkeys(G.get_vertices(), {})
    vertices = frozenset(G.get_vertices()) - {start}
    # N = G.num_vertices()

    for k in vertices:
        cost[k][frozenset([k])] = D[start][k]
    subsets = powerset(vertices, min_size=2)
    for s in subsets:
        S = frozenset(s)
        print(f"\nConsidering set {S}")
        for k in s:
            no_k = S - {k}
            print(f"S without {k}: {no_k}")
            cost[k][S] = min([cost[m][no_k] + D[m][k] for m in no_k])
            print(f"Cost from {S} to {k}: {cost[k][S]}")
    opt = min([cost[k][vertices] + D[k][start] for k in vertices])
    return opt

def held_karp2(G, D, start):
    cost = {}
    parent = {}
    for v in G.vertices():
        cost[v] = {}
        parent[v] = {}
    vertices = frozenset(G.vertices()) - {start}
    # N = G.num_vertices()

    for k in vertices:
        if not k == start:    
            cost[k][frozenset()] = D[start][k]
            parent[k][frozenset()] = start

    subsets = powerset(vertices, min_size=1)
    subset_size = 1
    for s in subsets:
        if len(s) > subset_size:
            subset_size += 1
            print(f"\nCurrent Subset size: {len(s)}")
        S = frozenset(s)
        for k in vertices - S:
            c = inf
            p = None
            for m in S:
                if not m == k:
                    x = cost[m][S - {m}] + D[m][k]
                    if x < c:
                        c = x
                        p = m
            cost[k][S] = c
            parent[k][S] = p
    min_cost = inf
    initial_parent = None
    for k in vertices:
        c = cost[k][vertices - {k}] + D[k][start]
        if c < min_cost:
            min_cost = c
            initial_parent = k
    
    # rebuild path
    tour = [start]
    S = vertices
    n = initial_parent
    while not n == start:
        tour.append(n)
        S = S - {n}
        n = parent[n][S]
    tour.append(start)
    tour.reverse()
    for v in tour:
        tour_indices = [int(v) for v in tour]


    return (tour_indices, min_cost)

if __name__ == "__main__":
    pass