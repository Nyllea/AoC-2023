input_file_path = "Day8/input.txt"

direction_dict = {'L':0, 'R':1} # The indexes corresponding to each direction
starting_node = "AAA"
end_node = "ZZZ"

f = open(input_file_path, "r")
lines = f.read().splitlines()

instructions_str = lines[0]
network_str = lines[2:]

nodes_directions_dict = dict() # Dictionnary containing the two reachable nodes (left,right) from a given node

# Creation of the newtork by filling nodes_directions_dict
for node_line in network_str:
    node_infos = node_line.split(" = ")
    node_out = node_infos[1][1:-1].split(", ")

    node_name = node_infos[0]
    node_out_left = node_out[0]
    node_out_right = node_out[1]
    
    nodes_directions_dict[node_name] = (node_out_left, node_out_right)

# Conversion of the instructions to a corresponding list of indexes for nodes_directions_dict
instructions = [direction_dict[dir] for dir in instructions_str]
nbr_of_instructions = len(instructions)

# Graph traversal along the given path, unil the end is met
current_node = starting_node
instr_id = 0 # Index of the current instruction
nbr_of_steps = 0
while current_node != end_node:
    possible_directions = nodes_directions_dict[current_node]
    current_node = possible_directions[instructions[instr_id]]

    instr_id = (instr_id + 1) % nbr_of_instructions
    nbr_of_steps += 1

print(nbr_of_steps)