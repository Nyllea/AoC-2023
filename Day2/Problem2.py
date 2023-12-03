input_file_path = "Day2/input.txt"

# All the possible cube colors, with their default amont to 0
possible_colors = {"red": 0, "green": 0, "blue": 0}

f = open(input_file_path, "r")
lines = f.read().splitlines()

sum_of_powers = 0
for line in lines:
    game_line = line.split(":")

    game_id = int(game_line[0].split(" ")[-1])
    
    # List of the results of the game, each element is a set of cubes revealed from the bag
    game_results = game_line[-1].split(";")

    # Minimum amount of cube of each color needed for this game to be possible
    min_cubes_needed = possible_colors.copy()
    
    for cube_set in game_results:
        result_cubes = cube_set.split(",")
        for cube in result_cubes:
            cube_values = cube.split(" ")
            cube_amount = int(cube_values[1])
            cube_color = cube_values[-1]

            # Make sure the cube is not an unprovided color
            if not cube_color in min_cubes_needed:
                print("The color ", cube_color, " from game ", game_id, " is unknown")
                exit()

            # Actualize the minimum amount of cubes of this color needed for this game
            min_cubes_needed[cube_color] = max(min_cubes_needed[cube_color], cube_amount)
        
    # Calculate the power of the minimum set of cubes of the game
    game_power = 1
    for min_amount in min_cubes_needed.values():
        game_power *= min_amount
    
    sum_of_powers += game_power

print(sum_of_powers)            
