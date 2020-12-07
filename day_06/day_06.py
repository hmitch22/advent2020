import sys

def part_a(file_name):
    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print("File", file_name, "could not be found. Skipping.")
        return -1

    count = 0
    current_questions = []
    for line in file:
        line = line.replace("\n", "")

        if len(line) == 0:
            # Marks the end of the previous passport - check if valid
            count += len(current_questions)
            current_questions = []
        else:
            # Continue to parse lines into data fields
            try:
                if not line.isalpha() or not line.islower():
                    print("File", file_name, "contains invalid characters or invalid syntax - skipping.")
                    return -1

                for char in line:
                    if char not in current_questions:
                        current_questions.append(char)
            except ValueError:
                file.close()
                print("File", file_name, "is not in the expected format - please check for errors")
                return None

    file.close()

    if len(current_questions) != 0:
        count += len(current_questions)

    return count


def part_b(file_name):
    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print("File", file_name, "could not be found. Skipping.")
        return -1

    count = 0
    current_questions = []
    first_person = True
    for line in file:
        line = line.replace("\n", "")

        if len(line) == 0:
            # Marks the end of the previous passport - check if valid
            count += len(current_questions)
            current_questions = []
            first_person = True
        else:
            # Continue to parse lines into data fields
            try:
                if not line.isalpha() or not line.islower():
                    print("File", file_name, "contains invalid characters or invalid syntax - skipping.")
                    return -1

                if first_person:
                    first_person = False
                    for char in line:
                        if char not in current_questions:
                            current_questions.append(char)
                else:
                    index = 0
                    while index < len(current_questions):
                        char = current_questions[index]
                        if char not in line:
                            current_questions.pop(index)
                        else:
                            index += 1
            except ValueError:
                file.close()
                print("File", file_name, "is not in the expected format - please check for errors")
                return None

    file.close()

    if len(current_questions) != 0:
        count += len(current_questions)

    return count


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Number of arguments invalid.")
        print("Please provide the path of at least one valid input file")
        print("i.e. day_06.py input.txt")

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