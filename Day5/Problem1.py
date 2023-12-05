input_file_path = "Day5/input.txt"

f = open(input_file_path, "r")
lines = f.read().splitlines()

# Two lists containing the values we are looking for in each map from the input
values_to_look_for = []
next_values_to_look_for = []

for line in lines:
    title_line = line.split(":")

    # If the line is a title
    if len(title_line) == 2:
        seed_line = title_line[1].split(" ")

        # If it's the seed line, we add the seeds to the list of values we will be looking for
        if len(seed_line) > 1:
            for seed_nbr in seed_line:
                if seed_nbr.isdigit():
                    next_values_to_look_for += [int(seed_nbr)]
        else:
            # We add the values that weren't mapped as they are
            next_values_to_look_for += values_to_look_for

            # We actualize the values we are looking for
            values_to_look_for = next_values_to_look_for
            next_values_to_look_for = []
    else:
        numbers = line.split(" ")

        # If it's a valid line (and not an empty one)
        if len(numbers) == 3:
            map_destination_start = int(numbers[0])
            map_source_start = int(numbers[1])
            map_range_len = int(numbers[2])

            temp_values_to_look_for = values_to_look_for.copy()
            for look_for_val in temp_values_to_look_for:
                # If the value we are looking for falls within the source range of the map,
                # we add it's mapped value to the values we will be looking for in the next map,
                # and remove that value from the values we are looking for
                if look_for_val >= map_source_start and look_for_val < map_source_start + map_range_len:
                    next_values_to_look_for += [map_destination_start + look_for_val - map_source_start]
                    values_to_look_for.remove(look_for_val)

values_to_look_for += next_values_to_look_for

print(min(values_to_look_for))