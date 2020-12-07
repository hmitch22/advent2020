# File IO sucks

import sys


def part_a(file_name, color_name):
    outer_to_inner, inner_to_outer = get_color_maps(file_name)

    valid_containers = inner_to_outer[color_name].copy()
    containers_to_check = valid_containers.copy()

    while len(containers_to_check) > 0:
        container = containers_to_check.pop()

        if container in inner_to_outer:
            also_valid = inner_to_outer[container]

            for valid_outer_bag in also_valid:
                if valid_outer_bag not in valid_containers:
                    containers_to_check.append(valid_outer_bag)
                    valid_containers.append(valid_outer_bag)

    return len(valid_containers)


def part_b(file_name, color_name):
    outer_to_inner, inner_to_outer = get_color_maps(file_name)

    def get_bag_count(clr):
        bags_needed = outer_to_inner[clr]
        if len(bags_needed) == 0:
            return 1

        count = 0

        for bag_array in bags_needed:
            bag_count = bag_array[0]
            bag_color = bag_array[1]

            count += bag_count * get_bag_count(bag_color)

        return count + 1

    return get_bag_count(color_name) - 1


def get_color_maps(file_name):
    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print("File", file_name, "could not be found. Skipping.")
        return -1

    outer_to_inner = {}
    inner_to_outer = {}

    for line in file:
        # Remove unnecessary words
        line = line.replace("\n", "")
        line = line.replace(" bags", "")
        line = line.replace(" bag", "")
        line = line.replace(".", "")
        line = line.replace("  ", " ")

        if len(line) == 0:
            pass
        else:
            # Continue to parse lines into data fields
            try:
                outer_inner_split = line.split(" contain ")

                if len(outer_inner_split) != 2:
                    raise ValueError("File does not contain the correct format")

                outer_bag = outer_inner_split[0]
                inner_strings = outer_inner_split[1].split(", ")

                inner_bags = []

                if inner_strings[0] != "no other":
                    for inner_string in inner_strings:
                        array = inner_string.split(" ", maxsplit=1)
                        inner_bag = [int(array[0]), array[1]]
                        inner_bags.append(inner_bag)

                        if inner_bag[1] in inner_to_outer:
                            inner_to_outer[inner_bag[1]].append(outer_bag)
                        else:
                            inner_to_outer[inner_bag[1]] = [outer_bag]

                outer_to_inner[outer_bag] = inner_bags

            except ValueError:
                file.close()
                print("File", file_name, "is not in the expected format - please check for errors")
                return None

    file.close()

    return outer_to_inner, inner_to_outer


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Number of arguments invalid.")
        print("Please provide the path of at least one valid input file")
        print("i.e. day_07.py input.txt")

        exit(0)

    color = "shiny gold"

    print("Attempting to find solutions for", len(sys.argv) - 1, "input files")
    print("\nPart A:")
    for i in range(1, len(sys.argv)):
        solution = part_a(sys.argv[i], color)

        if solution == -1:
            print("Unable to find solution for file", sys.argv[i])
        else:
            print(solution, "- solution for file", sys.argv[i])

    print("\nPart B:")
    for i in range(1, len(sys.argv)):
        solution = part_b(sys.argv[i], color)

        if solution == -1:
            print("Unable to find solution for file", sys.argv[i])
        else:
            print(solution, "- solution for file", sys.argv[i])