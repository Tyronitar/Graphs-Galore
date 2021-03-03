from graph_tool.all import *
from graph import PropertyType, graph_from_file, edges_from_file, new_basic_graph
from graph_utils import distance_matrix_weights, highlight_path
from tsp import held_karp, held_karp2

# exec(open("test_graphs.py").read())

if __name__ == "__main__":
    test1, test1_edge_weights = new_basic_graph("test_graph_1.txt", False)
    # graph_draw(test1, vertex_text = test1.vertex_index, edge_text=test1_edge_weights)
    test1_dist = distance_matrix_weights(test1, test1_edge_weights)
    test1_tour, test1_tour_cost = held_karp2(test1, test1_dist, test1.vertex(0))
    print(f"Test1\nShortest tour: {test1_tour}\nCost: {test1_tour_cost}\n")
    # print(held_karp2(test1, test1_dist, 0))

    test2, test2_edge_weights = new_basic_graph("test_graph_2.txt", True)
    # graph_draw(test2, vertex_text = test2.vertex_index, edge_text=test2_edge_weights)
    test2_dist = distance_matrix_weights(test2, test2_edge_weights)
    test2_tour, test2_tour_cost = held_karp2(test2, test2_dist, test2.vertex(0))
    print(f"Test2\nShortest tour: {test2_tour}\nCost: {test2_tour_cost}\n")
    test2_v_color, test2_e_color= highlight_path(test2, test2_tour)
    
    graph_draw(test2, vertex_text = test2.vertex_index,vertex_fill_color=test2_v_color,edge_color=test2_e_color,edge_text=test2_edge_weights)

    test3, test3_edge_weights = new_basic_graph("test_graph_3.txt", True)
    # graph_draw(test3, vertex_text = test3.vertex_index, edge_text=test3_edge_weights)
    test3_dist = distance_matrix_weights(test3, test3_edge_weights)
    test3_tour, test3_tour_cost = held_karp2(test3, test3_dist, test3.vertex(0))
    print(f"Test3\nShortest tour: {test3_tour}\nCost: {test3_tour_cost}\n")
    test3_v_color, test3_e_color= highlight_path(test3, test3_tour)
    
    graph_draw(test3, vertex_text = test3.vertex_index,vertex_fill_color=test3_v_color,edge_color=test3_e_color,edge_text=test3_edge_weights)
