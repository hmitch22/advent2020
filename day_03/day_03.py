# I'm bad at coding

import sys


def convert_file_to_array(file_name):
    # Note: this shouldn't be separated for efficient code. I chose to separate this for code reusability.
    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print("File", file_name, "could not be found. Skipping.")
        return None

    array = []
    line_length = -1

    for line in file:
        line = line.replace("\n", "")

        array.append(line)

        if line_length == -1:
            line_length = len(line)
        elif line_length != len(line):
            print("File", file_name, "contains lines of different lengths - all must be the same.")
            return None

        if line.count("#") + line.count(".") != line_length:
            print("File", file_name, "contains characters other than trees and spaces (# and .)")
            return None

    file.close()
    return array


def get_tree_count(array, slope):
    right, down = slope

    height = len(array)

    if height < down:
        return 0

    width = len(array[0])

    ind_x = 0
    ind_y = 0

    tree_count = 0
    while ind_y < height:
        # Check current position
        if array[ind_y][ind_x] == '#':
            tree_count += 1

        # Move positions, using modulo to stay within bounds
        ind_y += down
        ind_x += right
        ind_x = ind_x % width

    return tree_count

def part_a(file_name, right, down):
    array = convert_file_to_array(file_name)
    if array is None:
        return -1

    return get_tree_count(array, (right, down))


def part_b(file_name):
    array = convert_file_to_array(file_name)
    if array is None:
        return -1

    slopes = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]

    multiplication = 1

    for slope in slopes:
        tree_count = get_tree_count(array, slope)

        if tree_count < 0:
            return -1
        else:
            multiplication *= tree_count

    return multiplication

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Number of arguments invalid.")
        print("Please provide two integer slope number path of at least one valid input file")
        print("i.e. day_03.py 1 3 input.txt")

        exit(0)

    try:
        right_parameter = int(sys.argv[1])
        down_parameter = int(sys.argv[2])
        if right_parameter <= 0 or down_parameter <= 0:
            raise ValueError("Both numbers for the slope must be larger than 0.")
    except ValueError:
        print("Invalid value for slope - please provide two integers larger than 0")
        print("i.e. day_03.py 1 3 input.txt")
        exit(0)

    print("Attempting to find solutions for", len(sys.argv) - 3,
          'input files; slope of', right_parameter, down_parameter)

    print("\nPart A:")
    for i in range(3, len(sys.argv)):
        solution = part_a(sys.argv[i], right_parameter, down_parameter)

        if solution == -1:
            print("Unable to find solution for file", sys.argv[i])
        else:
            print(solution, "- solution for file", sys.argv[i])

    print("\nPart B:")
    for i in range(3, len(sys.argv)):
        solution = part_b(sys.argv[i])

        if solution == -1:
            print("Unable to find solution for file", sys.argv[i])
        else:
            print(solution, "- solution for file", sys.argv[i])