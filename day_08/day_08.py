import math
import sys


class Instruction:
    def __init__(self):
        self.operation = "nop"
        self.value = 0
        self.visited = False

    def set_operation(self, operation):
        self.operation = operation

    def get_operation(self):
        return self.operation

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def is_visited(self):
        return self.visited

    def set_visited(self, visited: bool):
        self.visited = visited

    def visit(self):
        self.visited = True


def get_instructions(file_name) -> list:
    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print("File", file_name, "could not be found. Skipping.")
        return None

    instructions = []
    for line in file:
        line = line.replace("\n", "")
        splits = line.split(" ")

        if len(splits) == 2:
            instr = Instruction()
            instr.set_operation(splits[0])

            value_string = splits[1]
            value = int(value_string[1:])
            if value_string[0] == "-":
                value *= -1

            instr.set_value(value)

            instructions.append(instr)

        else:
            print("File", file_name, "contains misformatted line: '", line, "'. Skipping.")

    return instructions


def reset_visited_flags(instructions):
    for instruction in instructions:
        instruction.set_visited(False)


# Function returns True if function executed without an infinite loop at the correct position (EOF)
def check_if_okay(instructions) -> (bool, int):
    operation_number = 0
    accumulator = 0
    while operation_number < len(instructions) and not instructions[operation_number].is_visited():
        instructions[operation_number].visit()
        inst = instructions[operation_number]

        if inst.get_operation() == "nop":
            operation_number += 1
        elif inst.get_operation() == "acc":
            accumulator += inst.get_value()
            operation_number += 1
        elif inst.get_operation() == "jmp":
            operation_number += inst.get_value()
        else:
            print("File contains unknown operation: '", inst.get_operation())
            return False, None

        if operation_number < 0:
            print("File contains invalid operation: at line:'", operation_number - inst.get_value())
            return False, None

    if operation_number == len(instructions):
        return True, accumulator
    else:
        return False, accumulator


def part_a(file_name):
    instructions = get_instructions(file_name)

    if instructions is None:
        return None

    file_is_okay, accumulator = check_if_okay(instructions)

    return accumulator


def part_b(file_name):
    instructions = get_instructions(file_name)

    if instructions is None:
        return None

    instructions_to_check = []
    for instr_pos in range(len(instructions)):
        instr = instructions[instr_pos]

        if instr.get_operation() == "nop" or instr.get_operation() == "jmp":
            instructions_to_check.append(instr_pos)

    for instr_pos in instructions_to_check:
        instr = instructions[instr_pos]

        if instr.get_operation() == "nop":
            instructions[instr_pos].set_operation("jmp")
        else:
            instructions[instr_pos].set_operation("nop")

        file_is_okay, accumulator = check_if_okay(instructions)

        if file_is_okay:
            print("Changing operationat line", instr_pos, "Fixed the file.")
            return accumulator
        else:
            reset_visited_flags(instructions)
            if instr.get_operation() == "nop":
                instructions[instr_pos].set_operation("jmp")
            else:
                instructions[instr_pos].set_operation("nop")

    return None


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Number of arguments invalid.")
        print("Please provide the path of at least one valid input file")
        print("i.e. day_08.py input.txt")

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