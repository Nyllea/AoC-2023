from math import ceil, floor, sqrt

input_file_path = "Day6/input.txt"

f = open(input_file_path, "r")
lines = f.read().splitlines()

total_time = lines[0].split(":")[1] # Total time of the race
best_distance = lines[1].split(":")[1] # Maximum distance travelled by the other boats

# Remove the spaces from the time and distance
total_time = total_time.replace(" ", "")
best_distance = best_distance.replace(" ", "")

total_time = int(total_time)
best_distance = int(best_distance)


# If the button is held for x ms, the speed is x mm/s and the time left is (T-x) ms (with T being the total time of the race)
# So the total distance travelled by the boat is x*(T-x)
# We thus need to find the number of integer solutions to the equation x*(T-x) > D, with D the maximum distance travelled by the other boats
# That means solving, for x integer, the equation x^2 - T*x + D < 0

# To do that, we first need to find x1 and x2 real solutions to x^2 - T*x + D = 0 (if they exist)
# Then, the solutions to our initial equation are all the x integer so that: x1 < x < x2

delta = total_time**2 - 4 * best_distance

# (delta<=0) means there is no real solution to this equation (delta<0) or only one real solution (delta=0)
# In this case, there is no integer solution satisfying the condition x1 < x < x2=x1
# ie there is no way to win the race in these conditions
if delta <= 0:
    nbr_ways_to_win = 0
else:
    # The two real solutions to the equation x^2 - T*x + D = 0
    # The value are naturally clamped to ]0, total_time] as long as the distance is positive
    min_time_held = (total_time - sqrt(delta))/2
    max_time_held = (total_time + sqrt(delta))/2

    # Compensate for the fact that we want < and not <= in our initial equation
    # ie the solutions of the real equation x^2 - T*x + D = 0 are to be excluded
    if min_time_held.is_integer():
        min_time_held += 1

    if max_time_held.is_integer():
        max_time_held -= 1

    # We can now calculate the number of possible ways to win the race
    nbr_ways_to_win = floor(max_time_held) - ceil(min_time_held) + 1    


print(nbr_ways_to_win)