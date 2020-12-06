# Again... Not optimal. Should be a better way of parsing the string. Maybe if error checking was reduced.

import sys


def part_a(file_name):
    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print("File", file_name, "could not be found. Skipping.")
        return -1

    count = 0
    for line in file:
        # First - attempt to parse line
        try:
            split_line = line.split("-", 1)
            if len(split_line) != 2:
                raise ValueError("String did not contain at least one hyphen.")
            least = int(split_line[0])
            line = split_line[1]

            split_line = line.split(" ", 2)
            if len(split_line) != 3:
                raise ValueError("String did not contain at least two spaces.")
            most = int(split_line[0])
            password = split_line[2]
            letter = split_line[1].replace(":", "")

            if most < 0 or least < 0:
                raise ValueError("Most and least must be larger than 0.")

            if len(letter) != 1 and letter.isalpha():
                raise ValueError("Character can only contain one alphanumeric.")

        except ValueError:
            file.close()
            print("File", file_name, "is not in the expected format - please check for errors")
            return None

        if least <= password.count(letter) <= most:
            count += 1

    file.close()
    return count


def part_b(file_name):
    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print("File", file_name, "could not be found. Skipping.")
        return -1

    count = 0
    for line in file:
        # First - attempt to parse line
        try:
            split_line = line.split("-", 1)
            if len(split_line) != 2:
                raise ValueError("String did not contain at least one hyphen.")
            ind1 = int(split_line[0])
            line = split_line[1]

            split_line = line.split(" ", 2)
            if len(split_line) != 3:
                raise ValueError("String did not contain at least two spaces.")
            ind2 = int(split_line[0])
            password = split_line[2]
            letter = split_line[1].replace(":", "")

            if ind1 < 0 or ind2 < 0:
                raise ValueError("ind1 and ind2 must be larger than 0.")

            if len(letter) != 1 and letter.isalpha():
                raise ValueError("Character can only contain one alphanumeric.")

        except ValueError:
            file.close()
            print("File", file_name, "is not in the expected format - please check for errors")
            return None

        if ind1 < len(password) or ind2 < len(password):
            if password[ind1 - 1] != letter and password[ind2 - 1] == letter:
                count += 1
            elif password[ind1 - 1] == letter and password[ind2 - 1] != letter:
                count += 1

    file.close()
    return count


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Number of arguments invalid.")
        print("Please provide the path of at least one valid input file")
        print("i.e. day_02.py input.txt")

        exit(0)

    print("Attempting to find solutions for", len(sys.argv) - 1, "input files")
    print("\nPart A:")
    for i in range(1, len(sys.argv)):
        solution = part_a(sys.argv[i])

        if solution == -1:
            print("Unable to find solution for file", sys.argv[i])
        else:
            print(solution, "- solution for file", sys.argv[i])

    print("\nPart B:")
    for i in range(1, len(sys.argv)):
        solution = part_b(sys.argv[i])

        if solution == -1:
            print("Unable to find solution for file", sys.argv[i])
        else:
            print(solution, "- solution for file", sys.argv[i])