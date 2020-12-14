import sys


def get_mask_numbers(mask_string) -> int:
    zero_mask = mask_string.replace("X", "1")
    one_mask = mask_string.replace("X", "0")
    return int(zero_mask, base=2), int(one_mask, base=2)


def get_possible_locations(location, mask_string):
    _, one_mask = get_mask_numbers(mask_string)
    location = location | one_mask

    possible_locations = []
    location_string = bin(location)[2:]

    while len(location_string) < len(mask_string):
        location_string = "0" + location_string

    float_indices = []

    for index in range(len(mask_string)):
        if mask_string[index] == "X":
            float_indices.append(index)

    float_values = 0
    while len(bin(float_values)) - 2 <= len(float_indices):
        binary_float_value = bin(float_values)[2:]
        while len(binary_float_value) < len(float_indices):
            binary_float_value = "0" + binary_float_value

        for binary_index in range(len(float_indices)):
            index = float_indices[binary_index]
            value = binary_float_value[binary_index]
            location_string = location_string[:index] + value + location_string[index + 1:]

        possible_locations.append(int(location_string, base=2))

        float_values += 1

    if len(float_indices) == 0:
        possible_locations.append(int(location_string, base=2))

    return possible_locations


def part_a(file_name):
    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print("File", file_name, "could not be found. Skipping.")
        return None

    memory = {}
    zero_mask = 0b111111111111111111111111111111111111
    one_mask = 0b0

    for line in file:
        line = line.replace("\n", "")
        split = line.split(" = ")
        instruction = split[0]
        value = split[1]

        if instruction == "mask":
            zero_mask, one_mask = get_mask_numbers(value)
        else:
            value = int(value)
            location = instruction.replace("mem[", "").replace("]", "")

            masked_value = value | one_mask
            masked_value = masked_value & zero_mask

            memory[location] = masked_value

    memory_sum = 0
    for key in memory:
        memory_sum += memory[key]

    return memory_sum


def part_b(file_name):
    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print("File", file_name, "could not be found. Skipping.")
        return None

    memory = {}
    mask = 0b0
    mask_string = ""

    for line in file:
        line = line.replace("\n", "")
        split = line.split(" = ")
        instruction = split[0]
        value = split[1]

        if instruction == "mask":
            _, mask = get_mask_numbers(value)
            mask_string = value
        else:
            value = int(value)
            location = int(instruction.replace("mem[", "").replace("]", ""))
            location = location | mask

            locations = get_possible_locations(location, mask_string)

            for loc in locations:
                memory[loc] = value

    memory_sum = 0
    for key in memory:
        memory_sum += memory[key]

    return memory_sum

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Number of arguments invalid.")
        print("Please provide the path of at least one valid input file")
        print("i.e. day_14.py input.txt")

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