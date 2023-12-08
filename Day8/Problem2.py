from math import lcm, inf

input_file_path = "Day8/input.txt"

direction_dict = {'L':0, 'R':1} # The indexes corresponding to each direction
start_node_character = 'A'
end_node_character = 'Z'

f = open(input_file_path, "r")
lines = f.read().splitlines()

instructions_str = lines[0]
network_str = lines[2:]

nodes_directions_dict = dict() # Dictionnary containing the two reachable nodes (left,right) from a given node
start_nodes = [] # List of all the start nodes
end_nodes = [] # List of all the end nodes

# Creation of the newtork by filling nodes_directions_dict, start_nodes and end_nodes
for node_line in network_str:
    node_infos = node_line.split(" = ")
    node_out = node_infos[1][1:-1].split(", ")

    node_name = node_infos[0]
    node_out_left = node_out[0]
    node_out_right = node_out[1]
    
    nodes_directions_dict[node_name] = (node_out_left, node_out_right)

    if node_name[-1] == start_node_character:
        start_nodes += [node_name]
    if node_name[-1] == end_node_character:
        end_nodes += [node_name]

# Conversion of the instructions to a corresponding list of indexes for nodes_directions_dict
instructions = [direction_dict[dir] for dir in instructions_str]

# all_nodes_steps is a 2D 'array' where each 'line' corresponds to a starting node, each 'column' to an end node
# and in each cell, it contains -1 if the end node is unreachable from the start node with the given path,
# otherwise, it contains the minimum number of steps to reach that end node

# 'Matrix' initialisation: we use a dictionnary to use the start and end node's names as keys
all_nodes_steps = dict()
for start_node in start_nodes:
    all_nodes_steps[start_node] = dict()
    for end_node in end_nodes:
        all_nodes_steps[start_node][end_node] = -1

# For each starting node, graph traversal along the given path, unil an end is met twice
# or we went through all the possible node/instruction combinations
nbr_of_instructions = len(instructions)
network_size = len(nodes_directions_dict)
for node in start_nodes:
    current_node = node
    instr_id = 0 # Index of the current instruction
    nbr_of_steps = 0

    met_end = [] # All of the end nodes met along the path
    while current_node not in met_end and nbr_of_steps < nbr_of_instructions*network_size:
        # If the current node is an end node, add it to the list of end met and actualize the 'matrix' all_nodes_steps
        if current_node[-1] == end_node_character:
            met_end.append(current_node)
            all_nodes_steps[node][current_node] = nbr_of_steps
 
        current_node = nodes_directions_dict[current_node][instructions[instr_id]]

        instr_id = (instr_id + 1) % nbr_of_instructions
        nbr_of_steps += 1


# Now we use all_nodes_steps to calculate iteratively, the minimum number of steps needed to reach one end node 
# AND so that the previous start nodes also reach an end node
# To do that, for each reachable end note, we use the least common multiple of the distance to that end node 
# and the previous minimum distance
# And we take the minimum of these values over all the reachable end nodes, for each start node
min_common_steps = 1
for start_node in start_nodes:
    current_min = inf
    for end_node in end_nodes:
        if all_nodes_steps[start_node][end_node] >= 0:
            current_min = min(current_min, lcm(min_common_steps, all_nodes_steps[start_node][end_node]))

    if current_min != inf: # if one end node is reachable
        min_common_steps = current_min
    else:
        print("The node", start_node, "cannot reach any end note")
        exit()

print(min_common_steps)