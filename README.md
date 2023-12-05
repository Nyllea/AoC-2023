
# AoC-2023

My solutions for the Advent of Code 2023 using python

## Files

Each day's solution is in it's own folder and contains:

- `test.txt`: The input of the example given in the problem of the day, used to easily test the code
- `input.txt`: The input for the actual problem of the day
- `Problem1.py`: My solution in python to the first problem
- `Problem2.py`: My solution in python to the second problem

## Output

Each python file prints only one value which is the solution to the problem of the day

## How to use

_Note: The following instructions assume that the terminal points to the main folder_

Every python file has a variable at the top named `input_file_path` which contains the path from the main directory to the input. 

By default, this value is set to the input of the file `input.txt` of the corresponding day. It is however possible to solve another input by changing this variable (to the test input for example, by changing the value of `input_file_path` to "DayX/test.txt").

Once the variable `input_file_path` is set, launch the corresponding python file

```bash
python DayX/ProblemN.py
```

with X the day wanted, and N = 1 or 2 the problem to solve.

