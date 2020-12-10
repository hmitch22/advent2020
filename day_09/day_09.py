# Learned/Relearned classes in Python! I should be able to do better going forward

import sys
import re
import math


def part_a(file_name, history_size):
    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print("File", file_name, "could not be found. Skipping.")
        return -1

    valid_history = []
    buffer_index = history_size

    for line in file:
        line = line.replace("\n", "")
        number = int(line)
        valid = False

        if len(valid_history) <= history_size:
            valid_history.append(number)

        if len(valid_history) > history_size:
            # Check if there are two numbers that sum to this new number
            possible_solutions = []

            for prev_index in range(history_size + 1):
                if prev_index == buffer_index:
                    # Ignore this value - it is too old to be valid
                    pass
                else:
                    old_value = valid_history[prev_index]
                    if old_value < number:
                        if old_value in possible_solutions:
                            # Number is valid
                            valid = True
                        else:
                            possible_solutions.append(number - old_value)

            if not valid:
                return number
            else:
                valid_history[buffer_index] = number
                buffer_index += 1
                buffer_index = buffer_index % (history_size + 1)

    return None


def part_b(file_name, history_size):
    sum = part_a(file_name, history_size)

    if sum is None:
        return None

    set_numbers = []
    set_sum = 0

    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print("File", file_name, "could not be found. Skipping.")
        return -1

    for line in file:
        line = line.replace("\n", "")
        number = int(line)

        set_sum += number
        set_numbers.append(number)

        while set_sum > sum:
            # Sum of the set is too large - remove numbers until it is smaller or equal
            set_sum -= set_numbers.pop(0)

        if set_sum == sum:
            min_val = -1
            max_val = -1

            for x in set_numbers:
                if x < min_val or min_val == -1:
                    min_val = x
                if x > max_val or max_val == -1:
                    max_val = x

            return min_val + max_val

    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Number of arguments invalid.")
        print("Please provide the path of at least one valid input file")
        print("i.e. day_09.py input.txt")

        exit(0)

    print("Attempting to find solutions for", len(sys.argv) - 1, "input files")
    print("\nPart A:")
    for i in range(1, len(sys.argv)):
        solution = part_a(sys.argv[i], 5)

        if solution is None:
            print("Unable to find solution for file", sys.argv[i])
        else:
            print(solution, "- solution for file", sys.argv[i])

    print("\nPart B:")
    for i in range(1, len(sys.argv)):
        solution = part_b(sys.argv[i], 25)

        if solution is None:
            print("Unable to find solution for file", sys.argv[i])
        else:
            print(solution, "- solution for file", sys.argv[i])