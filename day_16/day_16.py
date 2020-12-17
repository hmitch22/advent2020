# Variable names and logic can be unclear - may rewrite

import sys


class Field:
    def __init__(self, name, range1, range2):
        self.name = name

        self.range1_lower = int(range1[0])
        self.range1_upper = int(range1[1])

        self.range2_lower = int(range2[0])
        self.range2_upper = int(range2[1])

    def is_number_in_range(self, number):
        if self.range1_lower <= number <= self.range1_upper:
            return True

        if self.range2_lower <= number <= self.range2_upper:
            return True

        return False


def check_tickets(file_name, part_a):
    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print("File", file_name, "could not be found. Skipping.")
        return None

    all_fields = []
    all_valid_numbers = []

    line = file.readline()
    while line is not None:
        split = line.split(": ")

        if len(split) != 2:
            break

        field_name = split[0]
        split = split[1].split(" or ")

        range1 = split[0].split("-")
        range2 = split[1].split("-")

        field = Field(field_name, range1, range2)
        all_fields.append(field)

        for valid_num in range(int(range1[0]), int(range1[1]) + 1):
            if valid_num not in all_valid_numbers:
                all_valid_numbers.append(valid_num)

        for valid_num in range(int(range2[0]), int(range2[1]) + 1):
            if valid_num not in all_valid_numbers:
                all_valid_numbers.append(valid_num)

        line = file.readline()

    # your ticket:
    file.readline()
    your_ticket = file.readline()
    file.readline()
    file.readline()

    valid_tickets = []
    count = 0
    for line in file:
        line.replace("\n", "")

        ticket_numbers = line.split(",")
        valid = True

        for ticket_number in ticket_numbers:
            if int(ticket_number) not in all_valid_numbers:
                count += int(ticket_number)
                valid = False

        if valid:
            valid_tickets.append(ticket_numbers)

    if part_a:
        return count

    possible_columns = []
    for field in all_fields:
        cols = []
        for col in range(len(all_fields)):
            cols.append(col)
        possible_columns.append(cols)

    columns_to_find = len(all_fields)

    while columns_to_find > 0:
        columns_to_find = len(all_fields)

        for field_index in range(len(all_fields)):
            field = all_fields[field_index]
            current_possible_columns = possible_columns[field_index]

            if len(current_possible_columns) > 1:
                for valid_ticket in valid_tickets:
                    possible_columns_index = 0

                    while possible_columns_index < len(current_possible_columns):
                        col = current_possible_columns[possible_columns_index]
                        value = int(valid_ticket[col])

                        if not field.is_number_in_range(value):
                            current_possible_columns.remove(col)
                        else:
                            possible_columns_index += 1

                if len(current_possible_columns) == 1:
                    break

            if len(current_possible_columns) == 1:
                # Remove it from others
                columns_to_find -= 1
                for columns in possible_columns:
                    if current_possible_columns[0] in columns and columns != current_possible_columns:
                        columns.remove(current_possible_columns[0])

    multiplication = 1
    your_ticket = your_ticket.split(",")
    for field_index in range(len(all_fields)):
        field = all_fields[field_index]
        column = possible_columns[field_index][0]

        if field.name[0:9] == "departure":
            value = int(your_ticket[column])
            multiplication *= value

    return multiplication


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Number of arguments invalid.")
        print("Please provide the path of at least one valid input file")
        print("i.e. day_16.py input.txt")

        exit(0)

    print("Attempting to find solutions for", len(sys.argv) - 1, "input files")
    print("\nPart A:")
    for i in range(1, len(sys.argv)):
        solution = check_tickets(sys.argv[i], part_a=True)

        if solution is None:
            print("Unable to find solution for file", sys.argv[i])
        else:
            print(solution, "- solution for file", sys.argv[i])

    print("\nPart B:")
    for i in range(1, len(sys.argv)):
        solution = check_tickets(sys.argv[i], part_a=False)

        if solution is None:
            print("Unable to find solution for file", sys.argv[i])
        else:
            print(solution, "- solution for file", sys.argv[i])
