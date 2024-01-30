input_file_path = "Day14/input.txt"

rounded_rock = 'O'
cube_rock = '#'
empty_space = '.'

nbr_cycles = 1000000000


class Terrain:
    def __init__(self, terrain_width, terrain_height, square_pos, round_pos):
        # Make the terrain: the tuple represents respectively the linear id of the next available 
        # position when tilting up, left, down and right
        # The last element of the tuple indicates if the postion is occupied (True) or not (Fasle)
        self.terrain = [[-1,-1,-1,-1, False] for _ in range(terrain_height * terrain_width)]
        self.width = terrain_width
        self.height = terrain_height

        # Store the current position of all the rounded rocks
        self.rounded_pos = [x * terrain_width + y for (x,y) in rounded_pos]

        # Dictionnary with frozenset(rounded_pos) as key, and a cycle number as a value
        # Stores the cycle at which the given rounded_pos has last been attained
        # Used for cycle detection in the positions of the rounded rocks
        self.previous_rounded_pos = dict()
        

        # Placement of the square rocks
        for x,y in square_pos:
            lin_pos = x * terrain_width + y
            self.terrain[lin_pos] = [lin_pos,lin_pos,lin_pos,lin_pos, True]
        
        # Filling of the available positions on the whole terrain
        for i in range(terrain_height):
            last_left_tile_pos = i * terrain_width
            for j in range(terrain_width):
                lin_pos = i * terrain_width + j
                current_tile = self.terrain[lin_pos]

                # If a rock is at this position
                if current_tile[-1]:
                    last_left_tile_pos = lin_pos + 1
                else:
                    current_tile[1] = last_left_tile_pos
                    self.terrain[lin_pos] = current_tile

            last_right_tile_pos = i * terrain_width + terrain_width-1
            for j in range(terrain_width-1,-1,-1):
                lin_pos = i * terrain_width + j
                current_tile = self.terrain[lin_pos]

                # If a rock is at this position
                if current_tile[-1]:
                    last_right_tile_pos = lin_pos - 1
                else:
                    current_tile[3] = last_right_tile_pos
                    self.terrain[lin_pos] = current_tile
        
        for j in range(terrain_width):
            last_up_tile_pos = j
            for i in range(terrain_height):
                lin_pos = i * terrain_width + j
                current_tile = self.terrain[lin_pos]

                # If a rock is at this position
                if current_tile[-1]:
                    last_up_tile_pos = lin_pos + terrain_width
                else:
                    current_tile[0] = last_up_tile_pos
                    self.terrain[lin_pos] = current_tile

            last_down_tile_pos = (terrain_height-1) * terrain_width + j
            for i in range(terrain_height-1,-1,-1):
                lin_pos = i * terrain_width + j
                current_tile = self.terrain[lin_pos]

                # If a rock is at this position
                if current_tile[-1]:
                    last_down_tile_pos = lin_pos - terrain_width
                else:
                    current_tile[2] = last_down_tile_pos
                    self.terrain[lin_pos] = current_tile

        # Placement of the round rocks
        for lin_pos in self.rounded_pos:
            self.terrain[lin_pos][-1] = True

    # Removes a rock from the terrain and from the rounded_pos list
    # And returns the linear position of the rock
    def __remove_rock(self, rock_id):
        rock_pos = self.rounded_pos[rock_id]
        self.rounded_pos[rock_id] = -1
        self.terrain[rock_pos][-1] = False

        return rock_pos
    
    # Place the rock with the id rock_id at the position rock_pos
    def __place_rock(self, rock_id, rock_pos):
        self.rounded_pos[rock_id] = rock_pos
        self.terrain[rock_pos][-1] = True

    # Tilts the terrain in the required direction
    # 0 for up, 1 for left, 2 for down and 3 for right
    def tilt(self, direction):        
        for i in range(len(self.rounded_pos)):
            rounded_pos = self.__remove_rock(i)

            new_pos = self.terrain[rounded_pos][direction]
            while self.terrain[new_pos][-1]:
                if direction == 0:
                    new_pos = new_pos + self.width
                elif direction == 1:
                    new_pos = new_pos + 1
                elif direction == 2:
                    new_pos = new_pos - self.width
                elif direction == 3:
                    new_pos = new_pos - 1
            
            self.__place_rock(i, new_pos)

    # Makes a spin cycle, removes the rocks invariant by a spin cycle 
    # And returns True if a spin cycle let all the rocks invariant
    def spin_cycle(self, cycle_nbr=-1):
        # Make a whole spin cycle
        for direction in range(4):
            self.tilt(direction)

        # If the cycle_nbr is given, check for a repeating pattern in the positions of the rocks
        # By keeping track of all the previous positions in self.previous_rounded_pos
        if cycle_nbr != -1:
            # Use of the positions of all the rocks as a key, turned into a set to make the ordering irrelevant
            frozenset_rounded_pos = frozenset(self.rounded_pos)
            if frozenset_rounded_pos in self.previous_rounded_pos:
                return cycle_nbr - self.previous_rounded_pos[frozenset_rounded_pos]
            else:
                self.previous_rounded_pos[frozenset_rounded_pos] = cycle_nbr
                return -1

    # Returns the total load on the North support beam
    def total_north_load(self):
        total_load = 0
        for lin_pos in self.rounded_pos:
            x = lin_pos // self.width
            y = lin_pos % self.width

            total_load += self.height - x
        
        return total_load

    # Prints the current terrain
    def show(self):
        for x in range(self.height):
            line = ""
            for y in range(self.width):
                if x * self.width + y in self.rounded_pos:
                    line += 'O'
                elif self(x,y)[-1]:
                    line += '#'
                else:
                    line += '.'
            print(line)

    # Returns the value of the terrain at the given position (x,y)
    def __call__(self, x, y):
        if x < 0 or y < 0:
            print("can't use negative values")
            exit()
        
        return self.terrain[x * self.width + y]

# Reading of the input file to get the positions of the square and rounded rocks
f = open(input_file_path, "r")
lines = f.read().splitlines()

nbr_columns = len(lines[0])
nbr_rows = len(lines)

square_pos = []
rounded_pos = []
current_line = 0

for line in lines:
    for j in range(nbr_columns):
        element = line[j]
        if element == cube_rock:
            square_pos.append((current_line, j))
        
        elif element == rounded_rock:
            rounded_pos.append((current_line, j))

    current_line += 1

# Creation of the terrain
terrain = Terrain(nbr_columns, nbr_rows, square_pos, rounded_pos)

# Show the initial state of the terrain
# terrain.show()

# Iterate over spin cycles and stop the loop when a cycle has been found in the positions of the rounded rocks

# Number of spin cycles left after removing as many cycles as possible 
# using the found cycle in the positions of the rounded rocks
cycles_left = 0
for cycle in range(nbr_cycles):
    cycle_len = terrain.spin_cycle(cycle)

    # If a cycle is found
    if cycle_len != -1:
        cycles_left = (nbr_cycles-1 - cycle) % cycle_len
        print("Cycle found of length", cycle_len, "at cycle", cycle, ":", cycles_left, "cycles left to reach the final state")
        break

# Do the remaining cycles to reach nbr_cycles 
# after skipping as many spin cycles as possible using the cycle found in the positions of the rounded rocks
for cycle in range(cycles_left):
    terrain.spin_cycle()

# Show the final state of the terrain
# print()
# terrain.show()

# Print the total load on the north beam in the final state
print("Total load on the North beam in the final state :", terrain.total_north_load())