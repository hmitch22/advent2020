# Had to get a hint from the reddit to solve part b with the real input- I was unfamiliar with Chinese remainder theorem
# Learned a lot but not sure I would necessarily recognize another application if I was given a problem

import sys


def part_a(file_name):
    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print("File", file_name, "could not be found. Skipping.")
        return None

    timestamp = int(file.readline())
    bus_lines = file.readline().split(",")

    minimum_wait = None
    best_line = None

    for bus_line in bus_lines:
        if bus_line == "x":
            continue

        bus_line = int(bus_line)
        next_bus_wait = bus_line - (timestamp % bus_line)
        if minimum_wait is None or next_bus_wait < minimum_wait:
            best_line = bus_line
            minimum_wait = next_bus_wait

    return best_line * minimum_wait


def part_b_slow(file_name):
    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print("File", file_name, "could not be found. Skipping.")
        return None

    file.readline()
    bus_lines = file.readline().split(",")

    max_bus_line = None
    max_bus_line_index = None
    for index in range(len(bus_lines)):
        bus_line = bus_lines[index]
        if max_bus_line is None or (bus_line != "x" and int(bus_line) > max_bus_line):
            max_bus_line = int(bus_line)
            max_bus_line_index = index

    max_bus_line_t = max_bus_line
    time_t = 0
    constraints_satisfied = False
    while not constraints_satisfied:
        time_t = max_bus_line_t - max_bus_line_index

        for index in range(0, len(bus_lines)):
            line_number = bus_lines[index]
            if line_number == "x" or index == max_bus_line_index:
                if index == len(bus_lines) - 1:
                    constraints_satisfied = True
                continue

            line_number = int(line_number)

            if (time_t + index) % line_number != 0:
                break

            if index == len(bus_lines) - 1:
                constraints_satisfied = True

        max_bus_line_t += max_bus_line

    return time_t


def part_b(file_name):

    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print("File", file_name, "could not be found. Skipping.")
        return None

    file.readline()
    bus_lines = file.readline().split(",")
    m = 1
    terms = []
    non_x_lines = []

    for index in range(len(bus_lines)):
        bus_line = bus_lines[index]
        if bus_line == "x":
            continue
        m *= int(bus_line)
        terms.append(0)
        non_x_lines.append(int(bus_line))

    for index in range(len(non_x_lines)):
        bus_line = non_x_lines[index]
        terms[index] = int(m / bus_line)

    # For each term, see if it equals the right number mod the bus line
    term_index = 0
    for index in range(len(bus_lines)):
        bus_line = bus_lines[index]
        if bus_line == "x":
            continue
        bus_line = int(bus_line)

        term = terms[term_index]
        multiple_to_check = 2
        while term % bus_line != 1:
            term = terms[term_index] * multiple_to_check
            multiple_to_check += 1

        terms[term_index] = term
        term_index += 1

    terms_sum = 0
    term_index = 0
    for index in range(len(bus_lines)):
        bus_line = bus_lines[index]
        if bus_line == "x":
            continue

        bus_line = int(bus_line)

        terms_sum += (bus_line - index) * terms[term_index]
        term_index += 1

    while terms_sum - m > 0:
        terms_sum -= m

    return terms_sum


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Number of arguments invalid.")
        print("Please provide the path of at least one valid input file")
        print("i.e. day_13.py input.txt")

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
