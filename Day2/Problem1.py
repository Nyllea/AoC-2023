input_file_path = "Day2/input.txt"

amount_of_cubes = [("red", 12), ("green", 13), ("blue", 14)]

f = open(input_file_path, "r")
lines = f.read().splitlines()

valid_ids_sum = 0
for line in lines:
    game_line = line.split(":")

    game_id = int(game_line[0].split(" ")[-1])
    
    game_results = game_line[-1].split(";")
    
    game_is_valid = True
    for result in game_results:
        result_cubes = result.split(",")
        for cube in result_cubes:
            cube_values = cube.split(" ")
            cube_amount = int(cube_values[1])
            cube_color = cube_values[-1]

            color_is_valid = False
            for i in range(len(amount_of_cubes)):
                if cube_color == amount_of_cubes[i][0]:
                    color_is_valid = True
                    if cube_amount > amount_of_cubes[i][-1]:
                        game_is_valid = False
                        break
            
            if not color_is_valid:
                print("The color ", cube_color, " from game ", game_id, " is unknown")
                exit()
            
    if game_is_valid:
        valid_ids_sum += game_id
        #print(game_id)

print(valid_ids_sum)            
