input_file_path = "Day16/input.txt"

right_mirror = '/'
left_mirror = '\\'
vertical_splitter = '|'
horizontal_splitter = '-'
empty_pos = '.'

char_up = '^'
char_down = 'v'
char_left = '<'
char_right = '>'

initial_ray_pos = 0
initial_ray_dir = 1

# Stores the possible directions of the light ray
class Directions:
    def __init__(self, terrain_width):
        self.up = -terrain_width
        self.down = terrain_width
        self.right = 1
        self.left = -1

    def get_char(self, direction):
        if direction == self.up:
            return char_up
        elif direction == self.down:
            return char_down
        elif direction == self.left:
            return char_left
        elif direction == self.right:
            return char_right
        else:
            print("The direction", direction, "is unknown")
            exit()

# Class representing an obstacle, containing the new direction(s) of the light when it enconters it
class Obstacle:
    def __init__(self, directions, obstacle_char):
        # next_position is a dict with the direction in which the ray enters as keys, 
        # and returns the next direction(s) of the ray
        self.next_position = dict()

        if obstacle_char == right_mirror:
            self.char_value = right_mirror

            self.next_position[directions.right] = [directions.up]
            self.next_position[directions.left] = [directions.down]
            self.next_position[directions.up] = [directions.right]
            self.next_position[directions.down] = [directions.left]

        elif obstacle_char == left_mirror:
            self.char_value = left_mirror

            self.next_position[directions.right] = [directions.down]
            self.next_position[directions.left] = [directions.up]
            self.next_position[directions.up] = [directions.left]
            self.next_position[directions.down] = [directions.right]

        elif obstacle_char == vertical_splitter:
            self.char_value = vertical_splitter

            self.next_position[directions.right] = [directions.up, directions.down]
            self.next_position[directions.left] = [directions.up, directions.down]
            self.next_position[directions.up] = [directions.up]
            self.next_position[directions.down] = [directions.down]

        elif obstacle_char == horizontal_splitter:
            self.char_value = horizontal_splitter

            self.next_position[directions.right] = [directions.right]
            self.next_position[directions.left] = [directions.left]
            self.next_position[directions.up] = [directions.left, directions.right]
            self.next_position[directions.down] = [directions.left, directions.right]
        else:
            print("The obstacle '", obstacle_char, "' is not recognized")
            exit()


# Representation of the terrain with all the obstacles
class Terrain:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.directions = Directions(width)

        # Dictionnary with the obstacles positions as keys, and the corresponding obstacle class as values
        self.obstacles = dict()

        # Dictionnary of all the tiles met, with their positions as keys and the directions as values
        self.met_tiles = dict()


    # Returns true if the ray will get out of the terrain if it starts at position and goes in direction
    def __is_out_of_terrain(self, position, direction):
        y_pos = position // self.width
        x_pos = position % self.width

        if direction == self.directions.up:
            return y_pos <= 0
        elif direction == self.directions.down:
            return y_pos >= self.height-1
        elif direction == self.directions.right:
            return x_pos == self.width-1
        elif direction == self.directions.left:
            return x_pos == 0
        else:
            print("The direction", direction, "is unknown")
            exit()

    # Adds an obstacle to the terrain
    def add_obstacle(self, position, obstacle_char):
        self.obstacles[position] = Obstacle(self.directions, obstacle_char)

    # Adds a tile to the met tiles, with the corresponding direction
    def add_met_tile(self, position, direction):
        if position in self.met_tiles:
            self.met_tiles[position].add(direction)
        else:
            self.met_tiles[position] = {direction}

    # Returns true if the tile at position has been passed through with the given direction
    def __tile_met_with_dir(self, position, direction):
        return position in self.met_tiles and direction in self.met_tiles[position]
    
    # Adds the ray to ray_list if the new ray is in the terrain and doesn't make a loop
    def __add_ray(self, ray_list, old_position, new_direction):
        # If the new ray doesn't get out of the terrain
        if not self.__is_out_of_terrain(old_position, new_direction):
            new_pos = old_position + new_direction

            # If a ray didn't pass there already (to remove loops)
            if not self.__tile_met_with_dir(new_pos, new_direction):
                ray_list.append(LightRay(new_pos, new_direction))
                self.add_met_tile(new_pos, new_direction)

    # Returns the new positions of the given rays
    def next_pos(self, rays):
        new_rays = []
        for ray in rays:
            # If the ray passes an obstacle
            if ray.position in self.obstacles.keys():
                new_directions = self.obstacles[ray.position].next_position[ray.direction]

                for dir in new_directions:
                    self.__add_ray(new_rays, ray.position, dir)
            else:
                self.__add_ray(new_rays, ray.position, ray.direction)
        
        return new_rays
    
    # Return the number of energized tiles
    def energized_tiles(self):
        return len(self.met_tiles)
    
    # Prints the current terrain with all the met tiles and the direction in which the ray moved
    def show(self):
        print()
        for i in range(self.height):
            line = ""
            for j in range(self.width):
                position = i*self.width + j

                if position in self.obstacles:
                    line += self.obstacles[position].char_value
                elif position in self.met_tiles:
                    met_directions = self.met_tiles[position]

                    if len(met_directions) == 1:
                        for dir in met_directions:
                            line += self.directions.get_char(dir)
                            break
                    else:
                        line += str(len(met_directions))
                else:
                    line += empty_pos

            print(line)
                

# Representation of a single light ray
class LightRay:
    def __init__(self, position, direction):
        # Linear index corresponding to the position of the ray in the terrain
        self.position = position
        # Direction the ray is travelling towards (1 : right, -1 : left, terrain_height : down, -terrain_height : up)
        self.direction = direction


f = open(input_file_path, "r")
lines = f.read().splitlines()

height = len(lines)
width = len(lines[0])

# Terrain creation
terrain = Terrain(height, width)
current_position = 0
for line in lines:
    for character in line:
        # If there is an obstacle
        if character != empty_pos:
            terrain.add_obstacle(current_position, character)
        
        current_position += 1

terrain.show()

# Light ray creation
ray = LightRay(initial_ray_pos, initial_ray_dir)

# Move the ray(s) across the terrain
all_rays = [ray]
terrain.add_met_tile(ray.position, ray.direction)
while len(all_rays) != 0:
    all_rays = terrain.next_pos(all_rays)

terrain.show()

print(terrain.energized_tiles())