input_file_path = "Day15/input.txt"

remove_action = '-'
add_action = '='
nbr_of_boxes = 256

# Defining a class Lens to store the focal lenght and the label of a Lens
class Lens:
    def __init__(self, focal_length, label):
        self.focal_length = focal_length
        self.label = label

# Class Box storing the box number and the ordered list of lenses in the box
class Box:
    def __init__(self, box_nbr):
        self.box_nbr = box_nbr
        self.lenses = []
    
    # Removes the lens with the label 'label' from the box if it is in it
    def remove_lens(self, label):
        for lens in self.lenses:
            if lens.label == label:
                self.lenses.remove(lens)
    
    # If there is already a lens with the label 'label' in the box, replaces that lens with the new lens
    # Otherwise, adds a new lens with the required focal length and label at the end of the lenses in the box
    def add_lens(self, focal_length, label):
        lens_replaced = False
        for i in range(len(self.lenses)):
            if self.lenses[i].label == label:
                self.lenses[i].focal_length = focal_length
                lens_replaced = True
                break
        
        if not lens_replaced:
            self.lenses.append(Lens(focal_length, label))

    # Returns the sum of the focusing powers of all the lenses in the box
    def focusing_power(self):
        total_focusing_power = 0
        for i in range(len(self.lenses)):
            total_focusing_power += (1+self.box_nbr)*(1+i)*self.lenses[i].focal_length
        
        return total_focusing_power

# Uses the given algorithm to calculate the hash value of the string 'char_string'
def hash_algo(char_string):
    current_value = 0
    for character in char_string:
        current_value = ((current_value + ord(character)) * 17) % 256
    return current_value


f = open(input_file_path, "r")
lines = f.read().splitlines()

boxes = [Box(i) for i in range(nbr_of_boxes)] # List of all the boxes

for line in lines:
    init_sequence = line.split(',')
    
    # foreach step in the sequence
    for step in init_sequence:
        # Determines the action to perform
        if add_action in step:
            splitted_step = step.split(add_action)
            action = add_action
        elif remove_action in step:
            splitted_step = step.split(remove_action)
            action = remove_action
        else:
            print("No recognized action in the step :", step)
            exit()

        # Get the label and box number for this action
        label = splitted_step[0]
        box_nbr = int(hash_algo(label))

        # Perform the corresponding action
        if action == remove_action:
            boxes[box_nbr].remove_lens(label)
        elif action == add_action:
            focal_length = int(splitted_step[-1])
            boxes[box_nbr].add_lens(focal_length, label)

print(sum([box.focusing_power() for box in boxes]))
