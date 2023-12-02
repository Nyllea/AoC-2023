input_file_path = "Day2/input.txt"

possible_colors = ["red", "green", "blue"]

f = open(input_file_path, "r")
lines = f.read().splitlines()

sum_of_powers = 0
for line in lines:
    game_line = line.split(":")

    game_id = int(game_line[0].split(" ")[-1])
    
    game_results = game_line[-1].split(";")

    min_cubes_needed = []
    for color in possible_colors:
        min_cubes_needed += [(color, 0)]
    
    for result in game_results:
        result_cubes = result.split(",")
        for cube in result_cubes:
            cube_values = cube.split(" ")
            cube_amount = int(cube_values[1])
            cube_color = cube_values[-1]

            color_is_valid = False
            for i in range(len(min_cubes_needed)):
                if cube_color == min_cubes_needed[i][0]:
                    color_is_valid = True
                    new_amount = max(min_cubes_needed[i][-1], cube_amount)
                    min_cubes_needed[i] = (cube_color, new_amount)
            
            if not color_is_valid:
                print("The color ", cube_color, " from game ", game_id, " is unknown")
                exit()
            
    game_power = 1
    for (min_color, min_amount) in min_cubes_needed:
        game_power *= min_amount
        #print(game_id, min_color, min_amount)
    
    sum_of_powers += game_power

print(sum_of_powers)            
