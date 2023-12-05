input_file_path = "Day5/input.txt"

f = open(input_file_path, "r")
lines = f.read().splitlines()

# Two lists containing the ranges of values we are looking for in each map from the input
# in the form (range_start, range_lenght)
ranges_to_look_for = []
next_ranges_to_look_for = []

for line in lines:
    title_line = line.split(":")

    # If the line is a title
    if len(title_line) == 2:
        seed_line = title_line[1].split(" ")
        seed_line.remove('')

        # If it's the seed line, we look for it, we add the seeds ranges to the list of values we will be looking for
        if len(seed_line) > 1:
            for i in range(len(seed_line)//2):
                seed_start = int(seed_line[2*i])
                seed_range = int(seed_line[2*i+1])
                    
                next_ranges_to_look_for += [(seed_start, seed_range)]
        else:
            # We add the ranges that weren't mapped as they are
            next_ranges_to_look_for += ranges_to_look_for

            # We actualize the ranges we are looking for
            ranges_to_look_for = next_ranges_to_look_for
            next_ranges_to_look_for = []
    else:
        numbers = line.split(" ")

        # If it's a valid line (and not an empty one)
        if len(numbers) == 3:
            map_destination_start = int(numbers[0])
            map_source_start = int(numbers[1])
            map_range_len = int(numbers[2])

            temp_ranges_to_look_for = ranges_to_look_for.copy()
            for (range_val_start, range_val_len) in temp_ranges_to_look_for:
                # If there is an overlap of the range we are looking for and the mapped range
                if not (range_val_start >= map_source_start + map_range_len or range_val_start + range_val_len <= map_source_start):
                    # Calculate the part of the range we are looking for that is mapped
                    range_start_mapped = max(range_val_start, map_source_start)
                    range_start_destination_mapped = map_destination_start + range_start_mapped - map_source_start
                    range_len_mapped = min(map_source_start + map_range_len, range_val_start + range_val_len) - range_start_mapped

                    # Calculate the portion of the range before the mapped range
                    range_start_unmapped_before = range_val_start
                    range_len_unmapped_before = map_source_start - range_val_start

                    # Calculate the portion of the range after the mapped range
                    range_start_unmapped_after = map_source_start + map_range_len
                    range_len_unmapped_after = range_val_start + range_val_len - (map_source_start + map_range_len)

                    # Add the mapped range to the list of ranges we will be looking for
                    next_ranges_to_look_for += [(range_start_destination_mapped, range_len_mapped)]
                    ranges_to_look_for.remove((range_val_start, range_val_len))

                    # Add the range before the mapped range to the list of ranges we are still looking for
                    if range_len_unmapped_before > 0:
                        ranges_to_look_for += [(range_start_unmapped_before, range_len_unmapped_before)]
                    
                    # Add the range after the mapped range to the list of ranges we are still looking for
                    if range_len_unmapped_after > 0:
                        ranges_to_look_for += [(range_start_unmapped_after, range_len_unmapped_after)]


ranges_to_look_for += next_ranges_to_look_for

min_value = min(ranges_to_look_for)
print(min_value[0])