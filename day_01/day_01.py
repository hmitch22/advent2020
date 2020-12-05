# Definitely not the most efficient code - will attempt to do better other days.

import sys


def get_numbers(file_name):
    # Note: this shouldn't be separated for efficient code. I chose to separate this for code reusability.
    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print("File", file_name, "could not be found. Skipping.")
        return None

    all_numbers = []

    for line in file:
        try:
            num = int(line)
            if num < 0:
                raise ValueError("All numbers must be larger than 0.")
        except ValueError:
            file.close()
            print("File", file_name, "contains invalid characters - must all be integers larger than 0.")
            return None

        all_numbers.append(num)

    file.close()
    return all_numbers


def find_two_number_sum(numbers, sum_val):
    # numbers is an array of positive integers, sum val is a positive integer
    # returns -1 if no solution is found or one of the numbers that is part of the sum
    # Note: Other number is sum_val - returned number
    if len(numbers) < 2:
        return -1

    solutions = []

    for num in numbers:
        if num in solutions:
            # Sum has been found
            return num

        elif num < sum_val:
            solutions.append(sum_val - num)

    return -1


def part_a(file_name, sum_val):
    all_numbers = get_numbers(file_name)
    if all_numbers is None:
        return -1

    solution = find_two_number_sum(all_numbers, sum_val)

    if solution == -1:
        return -1
    else:
        return solution * (sum_val - solution)


def part_b(file_name, sum_val):
    all_numbers = get_numbers(file_name)
    if all_numbers is None:
        return -1

    while len(all_numbers) > 1:
        current_number = all_numbers.pop()

        if current_number < sum_val:
            solution = find_two_number_sum(all_numbers, sum_val - current_number)

            if solution == -1:
                pass
            else:
                return solution * (sum_val - solution - current_number) * current_number


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Number of arguments invalid.")
        print("Please provide the path of at least one valid input file and the sum to find")
        print("i.e. day_01.py 2020 input.txt")

        exit(0)

    try:
        sum_parameter = int(sys.argv[1])
        if sum_parameter < 0:
            raise ValueError("Sum must be larger than 0.")
    except ValueError:
        print("Invalid value for sum - please provide a valid integer larger than 0 for the sum to find.")
        print("i.e. day_01.py 2020 input.txt")
        exit(0)

    print("Attempting to find solutions for", len(sys.argv) - 2, 'input files; summing to', sum_parameter)
    print("\nPart A:")
    for i in range(2, len(sys.argv) - 1):
        solution = part_a(sys.argv[i], sum_parameter)

        if solution == -1:
            print("Unable to find solution for file", sys.argv[i])
        else:
            print(solution, "- solution for file", sys.argv[i])

    print("\n\nPart B:")
    for i in range(2, len(sys.argv) - 1):
        solution = part_b(sys.argv[i], sum_parameter)

        if solution == -1:
            print("Unable to find solution for file", sys.argv[i])
        else:
            print(solution, "- solution for file", sys.argv[i])

