input_file_path = "Day12/input.txt"

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
    # Remove all the empy/0 elements of the lists
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
    # First we simplify the line as much as possible by removing the elements that don't change the number of possibilities
    spring_line = [springs for springs in spring_line_str.split('.') if springs != ""]

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



f = open(input_file_path, "r")
lines = f.read().splitlines()

sum_possibilities = 0
i=0
for line in lines:
    springs_infos = line.split(' ')
    spring_line = springs_infos[0]
    nbr_damaged_springs = springs_infos[1].split(',')
    nbr_damaged_springs = [int(nbr) for nbr in nbr_damaged_springs]

    sum_possibilities += nbr_possibilities(spring_line, nbr_damaged_springs)

print(sum_possibilities)