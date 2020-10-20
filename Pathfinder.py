import matplotlib.pyplot as plt
import numpy as np
import SQLQueries as sql_access
import sys
from AllowMovements import AllowMovements

source_position = 0
target_position = 77
positions = []
sources_and_targets = []

def create_source_target_object():
    global sources_and_targets
    
    source_and_target_nodes = sql_access.get_source_and_targets()

    for node in source_and_target_nodes:
        source_and_target = AllowMovements()
        source_and_target.Source = tuple([node[0],node[1]])
        source_and_target.Target = tuple([node[2],node[3]])
        sources_and_targets.append(source_and_target)

def draw_positions(positions):
    for row in positions:
        plt.plot(row[0], row[1], "ro")   
        plt.ylabel("Y")
        plt.xlabel("X")
        
def draw_position(position, color):
    plt.plot(position[0], position[1], color)   
    plt.ylabel("Y")
    plt.xlabel("X")

def grab_all_target_nodes_with_source(source):
    global sources_and_targets
    nodes_with_source = []

    for node in sources_and_targets:
        if np.array_equal(node.Source,source) :
            nodes_with_source.append(node.Target)
    
    return nodes_with_source

def convert_tuple_to_float(to_convert):
    return tuple(map(float, to_convert))

def closest_node(target, nodes):

    closes_distance = sys.maxsize
    closes_point = sys.maxsize

    for target_node in nodes :
        converted_node = convert_tuple_to_float(target_node)
        converted_target = convert_tuple_to_float(target)

        distance = np.linalg.norm(np.subtract(converted_node, converted_target))

        if(distance < closes_distance):
            closes_distance = distance
            closes_point = target_node

    return closes_point

def all_valid_paths_between_points(source,target):

    complete_path = []

    while True:
        avalaible_movements = grab_all_target_nodes_with_source(source)
        closest_to_target = closest_node(target, avalaible_movements)

        if np.array_equal(target,closest_to_target) : break
        complete_path.append(closest_to_target)
        draw_position(closest_to_target,"go")
        source = closest_to_target

    return complete_path

def draw_full_path():
    source = positions[source_position]
    target = positions[target_position]

    draw_position(source,"bo")
    draw_position(target,"bo")
    
    all_valid_paths_between_points(source,target)

def InitialSetup():
    global positions
    sql_access.connect_with_database()
    positions = sql_access.get_positions()
    create_source_target_object()

def execute_graph_Positions():
    draw_positions(positions)
    draw_full_path()

InitialSetup()
execute_graph_Positions()

plt.show()