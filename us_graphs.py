from graph_tool.all import *
from graph import PropertyType, graph_from_file, edges_from_file
from math import floor
from graph_utils import dist, sort_by_degree, distance_matrix_pos
from four_color import sequential_coloring, RLF, RLF2
from pathfinding import Dijkstra
from tsp import held_karp2

# import py_compile
# py_compile.compile("tsp.py")
# exec(open("us_graphs.py").read())

def lower48(g, names):
    lower_48 = g.new_vertex_property("bool")
    for v in g.get_vertices():
        if names[v][-2:] == "AK" or names[v][-2:] == "HI":
            lower_48[v] = False
        else:
            lower_48[v] = True
    l48 = GraphView(g, vfilt=lambda v: lower_48[v])
    return l48

def get_state(g, names, state):
    state_ = g.new_vertex_property("bool")
    for v in g.get_vertices():
        if names[v][-2:] == state:
            state_[v] = True
        else:
            state_[v] = False
    state_gv = GraphView(g, vfilt=lambda v: state_[v])
    return state_gv

def color_by_state(g, names):
    state_ = g.new_vertex_property("string")
    with open("state abbreviations.txt") as file:
        line = file.readline()
        count = 1
        while line:
            state = line.rstrip("\n")
            for v in g.get_vertices():
                if state == names[v][-2:]:
                    color = "#{:02d}{:02d}{:02d}".format(floor((count / 13) * 100) % 99,count*2 % 100,floor((count / 5) * 100) % 100)
                    state_[v] = color
            line = file.readline()
            count += 1
    return state_
            

if __name__ == "__main__":
    output_size = (595,842)
    screen_output_size=(1500,800)

    counties, counties_props = graph_from_file("counties.txt", False, (PropertyType.Vertex, "string"),(PropertyType.Vertex, "float"),(PropertyType.Vertex, "vector<float>"))
    county_name_ = counties_props[0]
    county_fips_ = counties_props[1]
    county_pos_  = counties_props[2]
    edges_from_file(counties, "county_adjacency.txt", county_fips_)
    counties_lower = lower48(counties, county_name_)
    county_state = color_by_state(counties, county_name_)

    # graph_draw(counties, pos=county_pos_,output_size=output_size,vertex_fill_color=county_state, vertex_size=1.5, output="pdfs/counties_color_coded.pdf")
    # graph_draw(counties, pos=county_pos_,output_size=screen_output_size,vertex_fill_color=county_state, vertex_size=1.5)
    # graph_draw(counties_lower, pos=county_pos_,output_size=output_size,vertex_fill_color=county_state, vertex_size=3, output="pdfs/counties_lower48_color_coded.pdf")

    # graph_draw(counties, pos=county_pos_,output_size=output_size, vertex_size=1, output="pdfs/counties.pdf")
    # graph_draw(counties_lower, pos=county_pos_,output_size=output_size, vertex_size=1.5, output="pdfs/counties_lower48.pdf")

    states, states_props = graph_from_file("states.txt", False,(PropertyType.Vertex, "string"),(PropertyType.Vertex, "float"),(PropertyType.Vertex, "vector<float>"))
    state_name_ = states_props[0]
    state_num_ = states_props[1]
    state_pos_ = states_props[2]
    edges_from_file(states, "state_adjacency.txt", state_num_)
    states_lower_48 = lower48(states, state_name_)

    # graph_draw(states,vertex_text=state_name_,pos=state_pos_,output_size=output_size, output="pdfs/states.pdf")
    # graph_draw(states_lower_48,vertex_text=state_name_,pos=state_pos_,output_size=output_size, output="pdfs/states_lower48.pdf")
    
    # graph_draw(states,vertex_text=state_name_,pos=state_pos_,output_size=screen_output_size, vertex_size=15, output="pdfs/states.pdf")
    # graph_draw(states_lower_48,vertex_text=state_name_,pos=state_pos_,output_size=screen_output_size, vertex_size=20, output="pdfs/states_lower48.pdf")

    # state_counties = get_state(counties, county_name_, "HI")
    # graph_draw(state_counties,pos=county_pos_,output_size=output_size,vertex_size=12,output="pdfs/Individual States/hawaii.pdf")

    v1 = counties.vertex(1858)
    v2 = counties.vertex(204)
    # print(county_name_[v1])
    # print(state_pos_[v1])
    # print(county_name_[v2])
    # print(state_pos_[v2])
    # print(dist(v1, v2, state_pos_))

    v1_to_v2_vert, v1_to_v2_edge = Dijkstra(counties, county_pos_, v1, v2)
    v1v2_vertex_colors= counties.new_vertex_property("string")
    v1v2_edge_colors= counties.new_edge_property("string")
    for v in counties.get_vertices():
        if v1_to_v2_vert[v]:
            v1v2_vertex_colors[v] = "#0000FF"
        else:
            v1v2_vertex_colors[v] = "#FF0000"
    
    for e in counties.edges():
        if v1_to_v2_edge[e]:
            v1v2_edge_colors[e] = "#0000FF"
        else:
            v1v2_edge_colors[e] = "#000000"


    # graph_draw(counties,pos=county_pos_,vertex_fill_color = v1v2_vertex_colors,edge_color=v1v2_edge_colors, output_size=screen_output_size)

    # states_fct = sequential_coloring(states)
    # states_fct = RLF2(states, state_name_)
    # graph_draw(states,vertex_text=state_name_,pos=state_pos_,vertex_fill_color=states_fct,output_size=screen_output_size)
    # graph_draw(states,vertex_text=state_name_,pos=state_pos_,vertex_size = 5, vertex_fill_color=states_fct,output_size=output_size, output="pdfs/States Four Color Theorem.pdf")

    # counties_fct = sequential_coloring(counties)
    # counties_fct = RLF2(counties, county_name_)
    # graph_draw(counties,pos=county_pos_,vertex_fill_color = counties_fct, output_size=screen_output_size)
    # graph_draw(counties,pos=county_pos_,vertex_fill_color = counties_fct, vertex_size = 1.5, output_size=output_size, output="pdfs/Counties Four Color Theorem (five colors).pdf")

    states_lower_48_dist = distance_matrix_pos(states_lower_48, state_pos_)
    states_lower_48_tour,states_lower_48_tour_cost = held_karp2(states_lower_48, states_lower_48_dist, states_lower_48.vertex(21))
    print(f"Test2\nShortest tour: {states_lower_48_tour}\nCost: {states_lower_48_tour_cost}\n")
    