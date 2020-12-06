# Learned/Relearned classes in Python! I should be able to do better going forward

import sys
import re


class PassportField:
    def __init__(self, key, validation_function, parameters):
        self.key = key
        self.is_valid = validation_function
        self.params = parameters

    def value_valid(self, value):
        return self.is_valid(value, *self.params)


def is_number_valid(num_str, minimum, maximum, num_digits=-1, inc_leading_zeros=False):
    num_str = str(num_str)

    try:
        num = int(num_str)
    except ValueError:
        return False

    if inc_leading_zeros and num_digits != -1:
        if len(num_str) != num_digits:
            return False
    elif num_digits != -1:
        if len(str(num)) != num_digits:
            return False

    if minimum <= num <= maximum:
        return True
    else:
        return False


def is_height_valid(height):
    units = height[-2:]

    if units == "cm":
        return is_number_valid(height[:-2], 150, 193)
    elif units == "in":
        return is_number_valid(height[:-2], 59, 76)
    else:
        return False


def is_hair_color_valid(hair_color):
    x = re.search(r"#[0-9a-f]{6}", hair_color)
    if x is None:
        return False
    return x.group() == hair_color


def is_eye_color_valid(eye_color):
    return eye_color in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]


def is_passport_valid_a(passport):
    mandatory_fields = ["byr",
                        "iyr",
                        "eyr",
                        "hgt",
                        "hcl",
                        "ecl",
                        "pid",
                        ]
    optional_fields = ["cid",
                       ]

    for key in mandatory_fields:
        if key not in passport:
            # Passport did not contain one or more mandatory fields
            return False

        passport.pop(key)

    for key in passport:
        if key not in optional_fields:
            # Passport contained one or more fields that were not expected
            return False

    return True

def is_passport_valid_b(passport):
    mandatory_fields = {"byr": PassportField("byr", is_number_valid, (1920, 2002, 4, False)),
                        "iyr": PassportField("iyr", is_number_valid, (2010, 2020, 4, False)),
                        "eyr": PassportField("eyr", is_number_valid, (2020, 2030, 4, False)),
                        "hgt": PassportField("hgt", is_height_valid, ()),
                        "hcl": PassportField("hcl", is_hair_color_valid, ()),
                        "ecl": PassportField("hcl", is_eye_color_valid, ()),
                        "pid": PassportField("eyr", is_number_valid, (0, 999999999, 9, True)),
                        }
    optional_fields = {"cid": PassportField("cid", None, ()),
                       }

    for key in mandatory_fields:
        if key not in passport:
            # Passport did not contain one or more mandatory fields
            return False

        value = passport.pop(key)
        field = mandatory_fields[key]

        if field.is_valid is not None and not field.value_valid(value):
            return False

    for key in passport:
        if key not in optional_fields:
            # Passport contained one or more fields that were not expected
            return False

        value = passport[key]
        field = optional_fields[key]

        if field.is_valid is not None and not field.value_valid(value):
            return False

    return True


def check_passports(file_name, validation_function):
    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print("File", file_name, "could not be found. Skipping.")
        return -1

    count = 0
    current_passport = {}
    for line in file:
        line = line.replace("\n", "")

        if len(line) == 0:
            # Marks the end of the previous passport - check if valid
            if validation_function(current_passport):
                count += 1

            current_passport = {}
        else:
            # Continue to parse lines into data fields
            try:
                pairs = line.split(" ")

                for pair in pairs:
                    key_val = pair.split(":")

                    if len(key_val) != 2:
                        raise ValueError("Key Value pair did not contain the correct number of colons (1)")

                    key = key_val[0]
                    val = key_val[1]

                    if key in current_passport:
                        # Duplicate key - mark passport as invalid
                        current_passport["Passport Invalid"] = True
                    else:
                        current_passport[key] = val
            except ValueError:
                file.close()
                print("File", file_name, "is not in the expected format - please check for errors")
                return None

    file.close()

    if len(current_passport) != 0:
        if validation_function(current_passport):
            count += 1

    return count


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Number of arguments invalid.")
        print("Please provide the path of at least one valid input file")
        print("i.e. day_04.py input.txt")

        exit(0)

    print("Attempting to find solutions for", len(sys.argv) - 1, "input files")
    print("\nPart A:")
    for i in range(1, len(sys.argv)):
        solution = check_passports(sys.argv[i], is_passport_valid_a)

        if solution == -1:
            print("Unable to find solution for file", sys.argv[i])
        else:
            print(solution, "- solution for file", sys.argv[i])

    print("\n\nPart B:")
    for i in range(1, len(sys.argv)):
        solution = check_passports(sys.argv[i], is_passport_valid_b)

        if solution == -1:
            print("Unable to find solution for file", sys.argv[i])
        else:
            print(solution, "- solution for file", sys.argv[i])
