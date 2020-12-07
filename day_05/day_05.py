# Learned/Relearned classes in Python! I should be able to do better going forward

import sys
import re
import math


def get_row(row_str):
    max_row = 127
    min_row = 0
    for j in range(len(row_str)):
        char = row_str[j]
        if char == 'F':
            max_row -= math.ceil((max_row - min_row) / 2)
        else:
            min_row += math.ceil((max_row - min_row) / 2)

    return max_row


def get_col(col_str):
    max_col = 7
    min_col = 0

    for j in range(len(col_str)):
        char = col_str[j]
        if char == 'L':
            max_col -= math.ceil((max_col - min_col) / 2)
        else:
            min_col += math.ceil((max_col - min_col) / 2)

    return max_col


def part_a(file_name):
    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print("File", file_name, "could not be found. Skipping.")
        return -1

    max_seat_id = -1
    for line in file:
        line = line.replace("\n", "")

        x = re.search(r"[BF]{7}[LR]{3}", line)
        if x is None or x.group() != line:
            print("File", file_name, "contains invalid characters or invalid syntax - skipping.")
            return -1

        row = get_row(line[0:7])
        col = get_col(line[7:10])

        seat_id = (row * 8) + col

        if max_seat_id < seat_id:
            max_seat_id = seat_id

    return max_seat_id


def part_b(file_name):
    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print("File", file_name, "could not be found. Skipping.")
        return -1

    tickets = []
    possible_solutions = []

    for line in file:
        line = line.replace("\n", "")

        x = re.search(r"[BF]{7}[LR]{3}", line)
        if x is None or x.group() != line:
            print("File", file_name, "contains invalid characters or invalid syntax - skipping.")
            return -1

        row = get_row(line[0:7])
        col = get_col(line[7:10])
        seat_id = (row * 8) + col
        tickets.append(seat_id)

    tickets.sort()

    for index in range(1, len(tickets)):
        prev_ticket = tickets[index - 1]
        curr_ticket = tickets[index]

        if curr_ticket - prev_ticket == 2:
            return curr_ticket - 1

    return -1


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Number of arguments invalid.")
        print("Please provide the path of at least one valid input file")
        print("i.e. day_05.py input.txt")

        exit(0)

    print("Attempting to find solutions for", len(sys.argv) - 1, "input files")
    print("\nPart A:")
    for i in range(1, len(sys.argv)):
        solution = part_a(sys.argv[i])

        if solution == -1:
            print("Unable to find solution for file", sys.argv[i])
        else:
            print(solution, "- solution for file", sys.argv[i])

    print("\n\nPart B:")
    for i in range(1, len(sys.argv)):
        solution = part_b(sys.argv[i])

        if solution == -1:
            print("Unable to find solution for file", sys.argv[i])
        else:
            print(solution, "- solution for file", sys.argv[i])