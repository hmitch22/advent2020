# Code is slow - will look into alternatives and maybe adjust

import sys


def part_a(file_name, final_turn):
    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print("File", file_name, "could not be found. Skipping.")
        return None

    initial_turns = file.readline().split(",")
    turn_number = 0
    last_turn = -1
    memory_game = {}

    for turn in initial_turns:
        current_turn = turn

        if last_turn != -1:
            memory_game[str(last_turn)] = turn_number - 1

        last_turn = current_turn
        turn_number += 1

    while turn_number < final_turn:
        if str(last_turn) in memory_game:
            current_turn = turn_number - memory_game[str(last_turn)] - 1
        else:
            current_turn = 0

        memory_game[str(last_turn)] = turn_number - 1
        last_turn = current_turn
        turn_number += 1

    return last_turn


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Number of arguments invalid.")
        print("Please provide the path of at least one valid input file")
        print("i.e. day_15.py input.txt")

        exit(0)

    print("Attempting to find solutions for", len(sys.argv) - 1, "input files")
    print("\nPart A:")
    for i in range(1, len(sys.argv)):
        solution = part_a(sys.argv[i], 2020)

        if solution is None:
            print("Unable to find solution for file", sys.argv[i])
        else:
            print(solution, "- solution for file", sys.argv[i])

    print("\nPart B:")
    for i in range(1, len(sys.argv)):
        solution = part_b(sys.argv[i], 30000000)

        if solution is None:
            print("Unable to find solution for file", sys.argv[i])
        else:
            print(solution, "- solution for file", sys.argv[i])
