from graph_tool.all import *
import io
import enum

class PropertyType(enum.Enum):
    Vertex = 1
    Edge = 2

def graph_from_file(filename, directed, *properties):
    g = Graph(directed=directed)
    prop_ = []
    for p in properties:
        prop_type = p[0]
        value_type = p[1]
        if prop_type == PropertyType.Vertex:
            prop = g.new_vertex_property(value_type)
        else:
            prop = g.new_edge_property(value_type)
        prop_.append(prop)
    
    with open(filename) as file:
        line = file.readline()
        while line:
            line_ = line.rstrip("\n").split(";")
            
            v = g.add_vertex()

            for i,prop in enumerate(prop_):
                value_ = line_[i].split(",")
                if "float" in properties[i][1]:
                    temp = [float(val) for val in value_]
                    value_= temp

                if len(value_) > 1:
                    prop[v] = value_
                else:
                    prop[v] = value_[0]
            
            line = file.readline()
    return (g,prop_)


def edges_from_file(g, filename, id_):
    id_to_vertex = {}
    for vertex in g.get_vertices():
        _id = id_[vertex]
        id_to_vertex[_id] = vertex
    
    with open(filename) as file:
        line = file.readline()
        curr = None
        while line:
            line_ = line.rstrip("\n").split("\t")

            if line_[0] != "":
                curr_id = float(line_[1].strip("\""))
                curr = id_to_vertex[curr_id]

                neighbor_id = float(line_[3].strip("\""))
                neighbor = id_to_vertex[neighbor_id]

                
                if curr != neighbor and neighbor not in g.vertex(curr).all_neighbors():
                    g.add_edge(curr, neighbor)
            else:
                neighbor_id = float(line_[3].strip("\""))
                neighbor = id_to_vertex[neighbor_id]
                if curr != neighbor and neighbor not in g.vertex(curr).all_neighbors():
                    g.add_edge(curr, neighbor)
            
            line = file.readline()

def new_basic_graph(filename, directed):
    g = Graph(directed=directed)
    edge_weights = g.new_edge_property("float")
    line_count = 0
    
    with open(filename) as file:
        line = file.readline()
        line_count += 1
        while line:
            if line_count == 1:
                num = int(line.rstrip("\n"))
                for i in range(num):
                    g.add_vertex()
            else:
                line_ = line.rstrip("\n").split(":")
                print(line_)
                e = g.add_edge(int(line_[0]), int(line_[1]))
                edge_weights[e] = float(line_[2])
            
            line = file.readline()
            line_count += 1 
    return (g, edge_weights)



if __name__ == "__main__":
   pass