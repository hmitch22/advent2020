import sys
import re
import math


def get_adapter_list(file_name) -> list:
    adapter_list = []

    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print("File", file_name, "could not be found. Skipping.")
        return []

    for line in file:
        line = line.replace("\n", "")

        if len(line) != 0:
            try:
                number = int(line)
            except ValueError:
                print("File", file_name, "contained non-numeric values. Skipping.")
                return []
            adapter_list.append(number)

    return adapter_list


# Function returns the number of differences (0, 1, 2, or 3 volts) for all adapters
# Assumes adapter list is sorted in low to high
def get_difference_counts(adapter_list: list) -> (int, int, int, int):
    difference_counts = [0, 0, 0, 0]

    for index in range(len(adapter_list) - 1):
        difference = adapter_list[index + 1] - adapter_list[index]

        if difference <= 3:
            difference_counts[difference] += 1

    return difference_counts[0], difference_counts[1], difference_counts[2], difference_counts[3]


def get_path_count(adapter_list: list) -> int:
    if len(adapter_list) == 0:
        return 0

    # Keeps count of the paths into each adapter
    paths_in = []
    for index in range(len(adapter_list)):
        paths_in.append(0)

    paths_in[0] = 1

    for index in range(len(adapter_list)):
        current_adapter = adapter_list[index]
        current_paths_in = paths_in[index]

        for next_adapter_index in range(index + 1, len(adapter_list)):
            if adapter_list[next_adapter_index] - current_adapter <= 3:
                paths_in[next_adapter_index] += current_paths_in
            else:
                break

    return paths_in[len(adapter_list) - 1]


def part_a(file_name):
    adapter_list = get_adapter_list(file_name)
    adapter_list.append(0)
    adapter_list.sort()
    adapter_list.append(adapter_list[len(adapter_list) - 1] + 3)

    _, one_jolt, _, three_jolt = get_difference_counts(adapter_list)

    return one_jolt * three_jolt


def part_b(file_name):
    adapter_list = get_adapter_list(file_name)
    adapter_list.append(0)
    adapter_list.sort()
    adapter_list.append(adapter_list[len(adapter_list) - 1] + 3)

    return get_path_count(adapter_list)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Number of arguments invalid.")
        print("Please provide the path of at least one valid input file")
        print("i.e. day_10.py input.txt")

        exit(0)

    print("Attempting to find solutions for", len(sys.argv) - 1, "input files")
    print("\nPart A:")
    for i in range(1, len(sys.argv)):
        solution = part_a(sys.argv[i])

        if solution is None:
            print("Unable to find solution for file", sys.argv[i])
        else:
            print(solution, "- solution for file", sys.argv[i])

    print("\nPart B:")
    for i in range(1, len(sys.argv)):
        solution = part_b(sys.argv[i])

        if solution is None:
            print("Unable to find solution for file", sys.argv[i])
        else:
            print(solution, "- solution for file", sys.argv[i])