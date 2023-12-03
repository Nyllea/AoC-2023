input_file_path = "Day2/input.txt"

# Maximum amount of each cube for a game to be valid
amount_of_cubes = {"red": 12, "green": 13, "blue": 14}

f = open(input_file_path, "r")
lines = f.read().splitlines()

valid_ids_sum = 0
for line in lines:
    game_line = line.split(":")

    game_id = int(game_line[0].split(" ")[-1])
    
    # List of the results of the game, each element is a set of cubes revealed from the bag
    game_results = game_line[-1].split(";")
    
    game_is_valid = True
    for cube_set in game_results:
        if not game_is_valid:
            continue

        cubes = cube_set.split(",")
        for cube in cubes:
            cube_values = cube.split(" ")
            cube_amount = int(cube_values[1])
            cube_color = cube_values[-1]
            
            # Make sure the cube is not an unprovided color
            if not cube_color in amount_of_cubes:
                print("The color ", cube_color, " from game ", game_id, " is unknown")
                exit()
            
            # The game is not valid if it requires more cube of this color than the amount provided
            if cube_amount > amount_of_cubes[cube_color]:
                game_is_valid = False
                break
        
    if game_is_valid:
        valid_ids_sum += game_id

print(valid_ids_sum)            
