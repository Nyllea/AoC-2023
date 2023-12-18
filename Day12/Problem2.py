import time

input_file_path = "Day12/input.txt"

# The number of time to repeat each line to get the new line
repeat_number = 5

# The maximum lenght of the line to start the binary tree search
max_calleable_length = 7

# Simplify the problem by removing the elements of spring_line too small to fit the required amount of #
# at the start and at the end of the line
def ensure_length_coherence(spring_line, nbr_damaged_springs):
    # If one of the list is empty, there is no element to remove
    if len(spring_line) == 0 or len(nbr_damaged_springs) == 0:
        return spring_line, nbr_damaged_springs

    for i in [0, -1]:
        # If there is a # in the line and we need to place as many # as the length of the line
        # Then there is only one possibility and we can remove the line
        while len(spring_line[i]) == nbr_damaged_springs[i] and '#' in spring_line[i]:
            # The formulation i+1:(spring_len+1)*i+spring_len returns 1:spring_len if i=0 (ie removes the first element)
            # and 0:spring_len-1 if i=-1 (ie removes the last element)
            spring_len = len(spring_line)
            spring_line = spring_line[i+1:(spring_len+1)*i+spring_len]
                
            nbr_len = len(nbr_damaged_springs)
            nbr_damaged_springs = nbr_damaged_springs[i+1:(nbr_len+1)*i+nbr_len]

            # If it was the last element that we just removed
            if spring_len == 1 or nbr_len == 1:
                # Then we now have at least one empty list, so no further simplification is possible
                return spring_line, nbr_damaged_springs


        # While there isn't enough characters to put the required amount of #
        while len(spring_line[i]) < nbr_damaged_springs[i]:
            # If there is a # in the line, then the problem is impossible
            if '#' in spring_line[i]:
                return [], [-1]
            
            # Otherwise, all the ? in this line are ., so we can remove them from the line
            else:
                spring_len = len(spring_line)

                # If it is the last line, then removing it will leave an empty list
                # So the problem is not possible to solve (since nbr_damaged_springs is not empty)
                if spring_len == 1:
                    return [], [-1]
                
                # Otherwise, we can remove the line from spring_line
                else:
                    spring_line = spring_line[i+1:(spring_len+1)*i+spring_len]
    
    return spring_line, nbr_damaged_springs

# Simplify a list of string representing the spring line by removing the elements that don't change the number of possibilities
# For exemple, a line starting with ### and the nbr_damaged_springs starting with 3: we can remove both...
# Input:
#   - simplified_spring_line: List of string, each string being a sequence of '?' and '#' 
#       and each element of the list representing a line of springs separated by one or more '.'
#   - nbr_damaged_springs: A list of int representing the number of damaged springs in simplified_spring_line, 
#       in order from left to right
#
# Output:
#   - simplified_spring_line: Simplified, smaller list of string, each string being a sequence of '?' and '#' 
#       and each element of the list representing a line of springs separated by one or more '.'
#       All the ? and # that could be removed without changing the number of possibilities have been
#   - simplified_nbr_damaged_springs: A list of int representing the number of damaged springs in simplified_spring_line, 
#       in order from left to right
def simplify_spring_line(spring_line, nbr_damaged_springs):
    # Remove all the empty/0 elements of the lists
    simplified_spring_line = [spring for spring in spring_line if spring != '']
    simplified_nbr_damaged_springs = [nbr for nbr in nbr_damaged_springs if nbr != 0]

    simplified_spring_line, simplified_nbr_damaged_springs = ensure_length_coherence(simplified_spring_line, simplified_nbr_damaged_springs)

    # If one of the list is empty, no further simplification is possibile
    if len(simplified_spring_line) == 0 or len(simplified_nbr_damaged_springs) == 0:
        return simplified_spring_line, simplified_nbr_damaged_springs

    # Simplyfy by removing the first few # (and the last few # for i=-1, 
    # but the comment will focus on the first few # for clarity (ie i=0), the problem being symmetric)
    for i in [0, -1]:
        # While the first element of the first line (or last element of the last line) is a #
        while len(simplified_spring_line[i]) > 0 and simplified_spring_line[i][i] == '#':
            line_len = len(simplified_spring_line[i])
            nbr_len = len(simplified_nbr_damaged_springs)

            # Since we called ensure_length_coherence, we know that the line is long enough to place the required number of damaged springs
            # ie simplified_nbr_damaged_springs[i] <= line_len

            # Since simplified_spring_line[i] is only made of # and ?, placing the first few damaged springs is 
            # equivalent to removing the first few elements (ie it doesn't change the number of possibilities), 
            # as well as removing the corresponding element in simplified_nbr_damaged_springs


            # If the line will be finished once we remove the first few elements, remove the line
            # from simplified_spring_line and simplified_nbr_damaged_springs
            if line_len == simplified_nbr_damaged_springs[i]:
                spring_len = len(simplified_spring_line)

                # The formula is made so that for i=0, we get the slice 1:spring_len
                # And for i=-1, we get 0:-1
                simplified_spring_line = simplified_spring_line[i+1:(spring_len+1)*i+spring_len]
                simplified_nbr_damaged_springs = simplified_nbr_damaged_springs[i+1:(nbr_len+1)*i+nbr_len]
        
            # Otherwise, we need to put a . at the end of the line of # (if we can)
            # Which is equivalent to removing up until after that .
            else:
                # Selects the index of the position to put a . into 
                # (simplified_nbr_damaged_springs[i] if i=0, -simplified_nbr_damaged_springs[i]-1 if i=-1)
                last_damaged_id = simplified_nbr_damaged_springs[i]*(2*i + 1) + i

                # If the element after the line of # is a ?
                if simplified_spring_line[i][last_damaged_id] == '?':
                    # Then we turn the ? into a . <=> we remove up to the ? from simplified_spring_line
                    # as well as the corresponding value from simplified_nbr_damaged_springs
                    simplified_spring_line[i] = simplified_spring_line[i][(last_damaged_id+1)*(i+1):(line_len-last_damaged_id)*i + line_len]
                    simplified_nbr_damaged_springs = simplified_nbr_damaged_springs[i+1:(nbr_len+1)*i + nbr_len]
                
                # If the element after the line of # is a #, then it is impossible to solve
                else:
                    return [], [-1]
            
            # Further simplify by removing the elements with size not matching with simplified_nbr_damaged_springs
            simplified_spring_line, simplified_nbr_damaged_springs = ensure_length_coherence(simplified_spring_line, simplified_nbr_damaged_springs)

            # If one of the two list is empty, we can't simplify anymore
            if len(simplified_spring_line) == 0 or len(simplified_nbr_damaged_springs) == 0:
                return simplified_spring_line, simplified_nbr_damaged_springs

    return simplified_spring_line, simplified_nbr_damaged_springs


# Returns the number of possibilities to fill in the ? in the string spring_line_str with the number
# of # specified in the ordered list of integer nbr_damaged_springs
# To do so, this function searches the binary tree of all the possibilities, while simplifying the problem at each step
# to cut the useless branches as early as possible and optimize the search
def nbr_possibilities(spring_line_str, nbr_damaged_springs):
    # First we split the string with '.' into a list of string (of # and ?), which removes the useless '.' from it
    spring_line = [springs for springs in spring_line_str.split('.') if springs != ""]

    nbr_of_symbols = sum([len(line) for line in spring_line])
    nbr_of_damaged = sum(nbr_damaged_springs)
    # If there is more damaged springs to place than the total number of # and ?, it is impossible to solve the problem
    if nbr_of_symbols < nbr_of_damaged:
        return 0

    # We then simplify the line as much as possible by removing the elements that don't change the number of possibilities
    simplified_spring_line, simplified_nbr_damaged_springs = simplify_spring_line(spring_line, nbr_damaged_springs)

    simplified_len = len(simplified_spring_line)
    nbr_damaged_len = len(simplified_nbr_damaged_springs)
    
    # if there is no more # to place, then there is only one possibility: all .
    if nbr_damaged_len == 0:
        # So we need to check if there is a # remaining: if so, it is impossible to solve
        hash_still_in = False
        for element in simplified_spring_line:
            if element.find('#') != -1:
                hash_still_in = True
                break

        # If there is still a # in the line, then it is impossible (0 possibilities)
        if hash_still_in:
            return 0
        else: # Otherwise, all the elements of the line are ?, so the only possibility is a line of .
            return 1
    
    # If there is still some # to place but no more element in the line, then it is impossible to solve
    elif simplified_len == 0:
        return 0

    # If there is some damaged springs to place and some elements in the line
    else:
        # Create the new spring line (string) with the first element being a ?
        new_spring_line_str = '.'.join(simplified_spring_line)

        # Then we try the 2 possible cases: ?=. and ?=#
        dot_spring_line = '.' + new_spring_line_str[1:]
        dot_possibilities = nbr_possibilities(dot_spring_line, simplified_nbr_damaged_springs)

        hash_spring_line = '#' + new_spring_line_str[1:]
        hash_possibilities = nbr_possibilities(hash_spring_line, simplified_nbr_damaged_springs)

        return dot_possibilities + hash_possibilities


# This recursive function uses the fact that the number of possibilities to place L blocks of # on a line of size S
# can be calculated from the number of possibilities to place the first i blocks of # on the first part of the line (of size S/2),
# and the last L-i blocks on the rest of the line (of size S/2 too)
# by doing the product and the sum of all the possibilities

# nbr_of_possibilities(S,L) = sum(i in [0, L]) nbr_of_possibilities(first(S/2),first(i)) * nbr_of_possibilities(last(S/2),last(L-i))
# with S the size of the spring_line, L the length of nbr_damaged_springs, 
# and nbr_of_possibilities(S,L) the number of possibilities to place L blocks of #  on a line of size S,
# first(S/2) meaning the first S/2 elements of the line of size S, and last(L-i) the last L-i elements of the numbers of blocks of # to place

# Some memoization is also used to avoid some recursive calls and calling the function nbr_possibilities as much as possible
# in order to improve time complexity (at the expense of spatial complexity, which isn't the main issue for this problem)

# Inputs:
#   - spring_line: List of string, each string being a sequence of '?' and '#' 
#       and each element of the list representing a line of springs separated by one or more '.'
#   - nbr_damaged_springs:  A list of int representing the number of damaged springs in simplified_spring_line, 
#       in order from left to right
#   - multiple_elements_dict: dictionnary used for memoization, retaining the already calculated possibilities
def memoized_nbr_possibilities(spring_line, nbr_damaged_springs, multiple_elements_dict={}):
    # Determine the current key for the memoization
    spring_tuple = tuple(spring_line)
    damaged_tuple = tuple(nbr_damaged_springs)
    current_key = (spring_tuple, damaged_tuple)

    # If the number of possibilities has already been calculated, return it
    if current_key in multiple_elements_dict:
        return multiple_elements_dict[current_key]


    spring_len = len(spring_line)

    # If the line is empty, then if there is no more # to place, there is only one possibility
    # But if there is one or more # to place, then it is impossible (0 possibilities)
    if spring_len == 0:
        if len(nbr_damaged_springs) == 0:
            possibilities = 1
        else:
            possibilities = 0
    
    # If there is only one block of # and ? in the line
    elif spring_len == 1:
        # If the block is not too long, calculate the number of possibilities by going through the binary tree of possible values of all the ?
        if len(spring_line[0]) <= max_calleable_length:
            possibilities = nbr_possibilities(spring_line[0], nbr_damaged_springs)

        # Otherwise, if the block is too long, we split it by doing the two possibilities for a ?: # and .
        else:
            # Get the first ? after the first max_calleable_length elements of the block
            first_interrogation = spring_line[0][max_calleable_length:].find('?')

            # If no ? was found after the max_calleable_length first characters of the block,
            # then the call to nbr_possibilities will be fast (the line will be simplified to a length smaller than max_calleable_length in one iteration)
            if first_interrogation == -1:
                possibilities = nbr_possibilities(spring_line[0], nbr_damaged_springs)

            # If a ? was found after the first few max_calleable_length characters
            else:
                # Get the id of that ? in the block
                id_first_interrogation = max_calleable_length + first_interrogation

                # We cut spring_line in 2 at that position and make a recursive call on the two possibilities: ?=. and ?=#
                hash_string = spring_line[0][:id_first_interrogation] + '#' + spring_line[0][id_first_interrogation+1:]
                hash_possibilities = memoized_nbr_possibilities([hash_string], nbr_damaged_springs, multiple_elements_dict)

                dot_line = [spring_line[0][:id_first_interrogation], spring_line[0][id_first_interrogation+1:]]
                dot_possibilities = memoized_nbr_possibilities(dot_line, nbr_damaged_springs, multiple_elements_dict)

                possibilities = hash_possibilities + dot_possibilities

    # If there is more than one block of # and ?
    else:
        damaged_len = len(nbr_damaged_springs)

        # If there is no more # to place
        if damaged_len == 0:
            # There will be no recursion in this call since nbr_damaged_springs is empty
            possibilities = nbr_possibilities('.'.join(spring_line), nbr_damaged_springs)

        # If there is still some damaged springs to place, and more than one block of ? and #
        else:
            # Cut the list of blocks of # and ? in 2, then use the formula explicited in the description of the function 
            # to calculate recursively the number of possibilities

            middle_index = len(spring_line)//2
            possibilities = 0

            for i in range(damaged_len + 1):
                # Calculate nbr_of_possibilities(first(S/2),first(i))
                left_possibility_i = memoized_nbr_possibilities(spring_line[:middle_index], nbr_damaged_springs[:i], multiple_elements_dict)

                # This test is to avoid a useless recursive call
                if left_possibility_i != 0:
                    # Calculate nbr_of_possibilities(last(S/2),last(L-i)) and add the product to the total number of possibilities
                    right_possibility_i = memoized_nbr_possibilities(spring_line[middle_index:], nbr_damaged_springs[i:], multiple_elements_dict)
                    possibilities += left_possibility_i*right_possibility_i

    # Add the value to the memoization dictionnary before returning it
    multiple_elements_dict[current_key] = possibilities
    return possibilities


f = open(input_file_path, "r")
lines = f.read().splitlines()

all_lines = len(lines)

sum_possibilities = 0
current_line=1
total_time = 0

for line in lines:
    springs_infos = line.split(' ')
    spring_line = springs_infos[0]
    nbr_damaged_springs = springs_infos[1].split(',')
    nbr_damaged_springs = [int(nbr) for nbr in nbr_damaged_springs]

    # Create the new line by repeating the input repeat_number times, separated by '?'
    # and by reapeating the number of damaged springs
    full_spring_line = '?'.join([spring_line for _ in range(repeat_number)])
    full_nbr_damaged_springs = [nbr for _ in range(repeat_number) for nbr in nbr_damaged_springs]

    # Show the progress of the calculation
    print(current_line, "/", all_lines)
    print(full_spring_line, full_nbr_damaged_springs)

    t1 = time.perf_counter()

    # Calculate the number of possibilities with the function memoized_nbr_possibilities which uses a recursive formula 
    # and memoization to speed up the calculation
    other_possibilities = memoized_nbr_possibilities([springs for springs in full_spring_line.split('.') if springs != ""], full_nbr_damaged_springs)

    t2 = time.perf_counter()

    sum_possibilities += other_possibilities
    total_time += t2-t1

    print("Alt in:", t2-t1, "s")
    print()

    current_line+=1

print("Total time:", total_time, "s")
print(sum_possibilities)