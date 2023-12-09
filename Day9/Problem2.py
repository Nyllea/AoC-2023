import math

input_file_path = "Day9/input.txt"

f = open(input_file_path, "r")
lines = f.read().splitlines()

sum_value = 0
for line in lines:
    sequence = line.split(" ")
    sequence = [int(elem) for elem in sequence]
    n = len(sequence)
    
    # Let a_i be the added values at the beginning of the sequence s_i (ie the values predicted in the past)
    #   (sequence s_0 is the input, then sequence s_(i+1) is build by difference from sequence s_i, until len(s_i)=1)
    # Let s(i,j) be the jth value of sequence i (meaning s(0,n-1) is the last value of sequence s_0)

    # For example, if the initial sequence is s_0 = [2 4 6 8 10], then 
    #   - n = len(s0) = 3
    #   - The following sequences are s_1 = [2 2 2 2], s_2 = [0 0 0], s_3 = [0 0], s_4 = [0]
    #   - s(0,0)=2, s(0,2)=6, s(1,2)=2, ...

    # Then, the sequence of (a_i) satisfies
    #   - a_n = 0
    #   - foreach i in [0, n-1], a_i = s(i,0) - a_(i+1)
    # That means that we have the relation
    #   a_0 = sum((-1)**k * s(k,0))

    # Now we need to find the value of s(k,0) for all k
    # To do that, we have
    #   - s_0 known, so we know all the s(0,i) for i in [0,n-1]
    #   - s(k,l) = s(k-1,l+1) - s(k-1,l) for k in [1,n-1], l in [0, n-k-2]
    
    # By visualizing the sequences in a triangle, we can recognize a form of Pascal triangle
    # We now try to find the number of times each value s(0,i) appears in a_0
    #   ie Foreach i, the number of s(0,i) in sum((-1)**k * s(k,0)) = s(0,0) - s(1,0) + ... = s(0,0) - [s(0,1)-s(0,0)] + ... 
    # This value corresponds to the binomial coeficients: s(0,i) appears binom(n,i+1) times in the sum
    # It is also worth noting that the sign in the sum alternates for each value, with s(0,0) positive
    # That means that the sign of s(0,i) is (-1)**i

    # We can now comput the value of a_0
    ### a_01 = sum([(-1)**(k) * math.comb(n,k+1) * sequence[k] for k in range(n)])



    # However, we can try to improve the performances a bit more
    # To do that, we use the fact the binom(n,k) = binom(n,n-k)
    # We can rearrange the sum as a_0 = sum(binom(n,k+1) * ((-1)**k * s(0,k) + (-1)**(n-k) * s(0,n-k-2)))
    # That way, we only need to call the function binom half of the time

    # We also need to be careful of indices since n might not be divisible by 2
    # and the first coeficient needed is binom(n,1) and not binom(n,0)
    #   - (n-1)//2 is the number of sum of two values needed
    #   - If (n-1)%2==0: We start with the value (-1)**(n-1) * binom(n,n) * s(0,n-1) = (-1)**(n-1) * s(0,n-1), then add the other values 2 by 2
    #   - If (n+1)%2!=0: We start with the value (-1)**(n-1) * s(0,n-1) + the middle value of the triangle 
    #       (-1)**((n-1)//2) * binom(n,(n-1)//2+1) * sequence[(n-1)//2], then add the other values 2 by 2

    if (n-1)%2==0:
        a_0 = (-1)**(n-1) * sequence[-1]
    else:
        middle_id = (n-1)//2
        a_0 = (-1)**(n-1) * sequence[-1] + (-1)**middle_id * math.comb(n,middle_id+1) * sequence[middle_id]
    
    for k in range(0, (n-1)//2):
        bin_coef = math.comb(n,k+1)
        a_0 += bin_coef * ((-1)**k * sequence[k] + (-1)**(n-k) * sequence[n-k-2])
    
    sum_value += a_0

print(sum_value)    
