# Learned/Relearned classes in Python! I should be able to do better going forward

import sys


def get_seats_strings(file_name):
    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print("File", file_name, "could not be found. Skipping.")
        return None

    seats = []

    for line in file:
        line = line.replace("\n", "")
        seats.append(line)

    return seats


def get_adjacent_occupied(seat_num, upper_row, middle_row, lower_row):
    min_adjacent_seat = seat_num - 1
    max_adjacent_seat = seat_num + 1
    if min_adjacent_seat < 0:
        min_adjacent_seat = 0

    if max_adjacent_seat >= len(middle_row):
        max_adjacent_seat = len(middle_row) - 1

    count = 0
    if upper_row is not None:
        count += upper_row[min_adjacent_seat:max_adjacent_seat + 1].count("#")

    if lower_row is not None:
        count += lower_row[min_adjacent_seat:max_adjacent_seat + 1].count("#")

    if min_adjacent_seat != seat_num and middle_row[min_adjacent_seat] == "#":
        count += 1
    if max_adjacent_seat != seat_num and middle_row[max_adjacent_seat] == "#":
        count += 1

    return count


def are_any_occupied_visible(seat_row, seat_col, seats):
    max_column = len(seats[0])
    max_row = len(seats)
    # N
    if seat_row != 0:
        for row in range(seat_row - 1, -1, -1):
            seat = seats[row][seat_col]
            if seat == "#":
                return True
            elif seat == "L":
                break

    # S
    if seat_row != max_row - 1:
        for row in range(seat_row + 1, max_row):
            seat = seats[row][seat_col]
            if seat == "#":
                return True
            elif seat == "L":
                break

    # W
    if seat_col != 0:
        for col in range(seat_col - 1, -1 , -1):
            seat = seats[seat_row][col]
            if seat == "#":
                return True
            elif seat == "L":
                break

    # E
    if seat_col != max_column - 1:
        for col in range(seat_col + 1, max_column):
            seat = seats[seat_row][col]
            if seat == "#":
                return True
            elif seat == "L":
                break

    # NE
    if seat_row != 0 and seat_col != max_column - 1:
        for difference in range(seat_row):
            row = seat_row - difference - 1
            col = seat_col + difference + 1

            if col >= max_column:
                break

            seat = seats[row][col]
            if seat == "#":
                return True
            elif seat == "L":
                break

    # NW
    if seat_row != 0 and seat_col != 0:
        for difference in range(seat_row):
            row = seat_row - difference - 1
            col = seat_col - difference - 1

            if col < 0:
                break

            seat = seats[row][col]
            if seat == "#":
                return True
            elif seat == "L":
                break

    # SE
    if seat_row != max_row - 1 and seat_col != max_column - 1:
        for difference in range(max_row - seat_row - 1):
            row = seat_row + difference + 1
            col = seat_col + difference + 1

            if col >= max_column:
                break

            seat = seats[row][col]
            if seat == "#":
                return True
            elif seat == "L":
                break

    # SW
    if seat_row != max_row - 1 and seat_col != 0:
        for difference in range(max_row - seat_row - 1):
            row = seat_row + difference + 1
            col = seat_col - difference - 1

            if col < 0:
                break

            seat = seats[row][col]
            if seat == "#":
                return True
            elif seat == "L":
                break

    return False


def get_visible_occupied_count(seat_row, seat_col, seats):
    max_column = len(seats[0])
    max_row = len(seats)
    count = 0

    # N
    if seat_row != 0:
        for row in range(seat_row - 1, -1, -1):
            seat = seats[row][seat_col]
            if seat == "#":
                count += 1
                break
            elif seat == "L":
                break

    # S
    if seat_row != max_row - 1:
        for row in range(seat_row + 1, max_row):
            seat = seats[row][seat_col]
            if seat == "#":
                count += 1
                break
            elif seat == "L":
                break

    # W
    if seat_col != 0:
        for col in range(seat_col - 1, -1, -1):
            seat = seats[seat_row][col]
            if seat == "#":
                count += 1
                break
            elif seat == "L":
                break

    # E
    if seat_col != max_column - 1:
        for col in range(seat_col + 1, max_column):
            seat = seats[seat_row][col]
            if seat == "#":
                count += 1
                break
            elif seat == "L":
                break

    # NE
    if seat_row != 0 and seat_col != max_column - 1:
        for difference in range(seat_row):
            row = seat_row - difference - 1
            col = seat_col + difference + 1

            if col >= max_column:
                break

            seat = seats[row][col]
            if seat == "#":
                count += 1
                break
            elif seat == "L":
                break

    # NW
    if seat_row != 0 and seat_col != 0:
        for difference in range(seat_row):
            row = seat_row - difference - 1
            col = seat_col - difference - 1

            if col < 0:
                break

            seat = seats[row][col]
            if seat == "#":
                count += 1
                break
            elif seat == "L":
                break

    # SE
    if seat_row != max_row - 1 and seat_col != max_column - 1:
        for difference in range(max_row - seat_row - 1):
            row = seat_row + difference + 1
            col = seat_col + difference + 1

            if col >= max_column:
                break

            seat = seats[row][col]
            if seat == "#":
                count += 1
                break
            elif seat == "L":
                break

    # SW
    if seat_row != max_row - 1 and seat_col != 0:
        for difference in range(max_row - seat_row - 1):
            row = seat_row + difference + 1
            col = seat_col - difference - 1

            if col < 0:
                break

            seat = seats[row][col]
            if seat == "#":
                count += 1
                break
            elif seat == "L":
                break

    return count


def part_a(file_name):
    seats = get_seats_strings(file_name)

    if seats is None or len(seats) == 0:
        return 0

    updated = True
    column_count = len(seats[0])
    occupied_count = 0

    while updated:
        updated = False
        new_rows = ["", "", ""]

        for row_index in range(len(seats)):
            lower_row = None
            middle_row = seats[row_index]
            upper_row = None

            new_rows[2] = middle_row

            if row_index != 0:
                lower_row = seats[row_index - 1]
            if row_index != len(seats) - 1:
                upper_row = seats[row_index + 1]

            for column_index in range(column_count):
                seat = seats[row_index][column_index]

                if seat == "L":
                    if get_adjacent_occupied(column_index, lower_row, middle_row, upper_row) == 0:
                        updated = True
                        new_rows[2] = new_rows[2][:column_index] + "#" + new_rows[2][column_index + 1:]
                        occupied_count += 1
                elif seat == "#":
                    if get_adjacent_occupied(column_index, lower_row, middle_row, upper_row) >= 4:
                        updated = True
                        new_rows[2] = new_rows[2][:column_index] + "L" + new_rows[2][column_index + 1:]
                        occupied_count -= 1

            if row_index > 1:
                seats[row_index - 2] = new_rows[0]

            new_rows[0] = new_rows[1]
            new_rows[1] = new_rows[2]
            new_rows[2] = ""

            if row_index == len(seats) - 1:
                seats[row_index - 1] = new_rows[0]
                seats[row_index] = new_rows[1]

    return occupied_count


def part_b(file_name):
    seats = get_seats_strings(file_name)

    if seats is None or len(seats) == 0:
        return 0

    updated = True
    column_count = len(seats[0])
    occupied_count = 0

    while updated:
        updated = False
        new_seats = []

        for row_index in range(len(seats)):
            new_seats.append(seats[row_index])

            for column_index in range(column_count):
                seat = seats[row_index][column_index]

                if seat == "L":
                    if not are_any_occupied_visible(row_index, column_index, seats):
                        updated = True
                        new_seats[row_index] = new_seats[row_index][:column_index] + "#" + new_seats[row_index][column_index + 1:]
                        occupied_count += 1
                elif seat == "#":
                    if get_visible_occupied_count(row_index, column_index, seats) >= 5:
                        updated = True
                        new_seats[row_index] = new_seats[row_index][:column_index] + "L" + new_seats[row_index][column_index + 1:]
                        occupied_count -= 1

        for row_index in range(len(seats)):
            seats[row_index] = new_seats[row_index]

    return occupied_count


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Number of arguments invalid.")
        print("Please provide the path of at least one valid input file")
        print("i.e. day_11.py input.txt")

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
