input_file_path = "Day2/input.txt"

possible_colors = ["red", "green", "blue"]

f = open(input_file_path, "r")
lines = f.read().splitlines()

sum_of_powers = 0
for line in lines:
    game_line = line.split(":")

    game_id = int(game_line[0].split(" ")[-1])
    
    # List of the results of the game, each element is a set of cubes revealed from the bag
    game_results = game_line[-1].split(";")

    # Minimum amount of cube of each color needed for this game to be possible
    min_cubes_needed = []
    for color in possible_colors:
        min_cubes_needed += [(color, 0)]
    
    for cube_set in game_results:
        result_cubes = cube_set.split(",")
        for cube in result_cubes:
            cube_values = cube.split(" ")
            cube_amount = int(cube_values[1])
            cube_color = cube_values[-1]

            color_is_valid = False # To make sure the cube is not an unprovided color
            for i in range(len(min_cubes_needed)):
                if cube_color == min_cubes_needed[i][0]:
                    color_is_valid = True

                    # Set the minimum amount of cube needed for this set to also be possible
                    new_amount = max(min_cubes_needed[i][-1], cube_amount)
                    min_cubes_needed[i] = (cube_color, new_amount)
            
            if not color_is_valid:
                print("The color ", cube_color, " from game ", game_id, " is unknown")
                exit()
            
    # Calculate the power of the minimum set of cubes of the game
    game_power = 1
    for (min_color, min_amount) in min_cubes_needed:
        game_power *= min_amount
    
    sum_of_powers += game_power

print(sum_of_powers)            
