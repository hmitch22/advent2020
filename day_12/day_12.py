# Learned/Relearned classes in Python! I should be able to do better going forward

import sys


class Boat:
    directions = ["N", "E", "S", "W"]

    # pos = [x coordinate, y coordinate]
    # so +x is East and -y is South

    def __init__(self, initial_direction, initial_pos):
        self.dir_ind = self.directions.index(initial_direction)
        self.pos = initial_pos

    def get_direction(self):
        return self.directions[self.dir_ind]

    def get_pos(self):
        return self.pos

    def rotate(self, direction, degrees):
        if degrees < 0:
            if direction == "L":
                direction = "R"
            else:
                direction = "L"
            degrees *= -1

        while degrees > 0:
            if direction == "L":
                self.turn_left()
            else:
                self.turn_right()
            degrees -= 90

    def turn_left(self):
        self.dir_ind -= 1
        self.dir_ind %= len(self.directions)

    def turn_right(self):
        self.dir_ind += 1
        self.dir_ind %= len(self.directions)

    def move_direction(self, direction, value):
        if direction == "S":
            self.pos[1] -= value
        elif direction == "N":
            self.pos[1] += value
        elif direction == "E":
            self.pos[0] += value
        else:
            self.pos[0] -= value

    def move_forward(self, value):
        self.move_direction(self.directions[self.dir_ind], value)


class BoatWaypoint:
    directions = ["N", "E", "S", "W"]

    # pos = [x coordinate, y coordinate]
    # boat_pos is relative to 0,0; wp_pos is relative to the boat
    # so +x is East and -y is South

    def __init__(self, initial_boat_pos, initial_wp_pos):
        self.wp_pos = initial_wp_pos
        self.boat_pos = initial_boat_pos

    def get_boat_pos(self):
        return self.boat_pos

    def get_wp_pos(self):
        return self.wp_pos

    def rotate_wp(self, direction, degrees):
        if degrees < 0:
            if direction == "L":
                direction = "R"
            else:
                direction = "L"
            degrees *= -1

        while degrees > 0:
            if direction == "L":
                self.rotate_wp_left()
            else:
                self.rotate_wp_right()
            degrees -= 90

    def rotate_wp_left(self):
        wp_x = self.wp_pos[0]
        self.wp_pos[0] = self.wp_pos[1] * -1
        self.wp_pos[1] = wp_x

    def rotate_wp_right(self):
        wp_x = self.wp_pos[0]
        self.wp_pos[0] = self.wp_pos[1]
        self.wp_pos[1] = wp_x * -1

    def move_wp_direction(self, direction, value):
        if direction == "S":
            self.wp_pos[1] -= value
        elif direction == "N":
            self.wp_pos[1] += value
        elif direction == "E":
            self.wp_pos[0] += value
        else:
            self.wp_pos[0] -= value

    def move_boat_to_wp(self, count):
        self.boat_pos = [self.boat_pos[0] + (self.wp_pos[0] * count), self.boat_pos[1] + (self.wp_pos[1] * count)]


def move_boat(file_name):
    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print("File", file_name, "could not be found. Skipping.")
        return None

    boat = Boat("E", [0, 0])

    for line in file:
        line = line.replace("\n", "")

        direction = line[0]
        value = int(line[1:])

        if direction == "L" or direction == "R":
            boat.rotate(direction, value)
        elif direction == "F":
            boat.move_forward(value)
        else:
            boat.move_direction(direction, value)

    return boat


def move_waypoint(file_name) -> list:
    try:
        file = open(file_name, "r")
    except FileNotFoundError:
        print("File", file_name, "could not be found. Skipping.")
        return None

    boat = BoatWaypoint([0, 0], [10, 1])

    for line in file:
        line = line.replace("\n", "")

        direction = line[0]
        value = int(line[1:])

        if direction == "L" or direction == "R":
            boat.rotate_wp(direction, value)
        elif direction == "F":
            boat.move_boat_to_wp(value)
        else:
            boat.move_wp_direction(direction, value)

    return boat.boat_pos


def get_manhattan(pos) -> int:
    return abs(pos[0]) + abs(pos[1])


def part_a(file_name):
    boat = move_boat(file_name)
    return get_manhattan(boat.get_pos())


def part_b(file_name):
    boat_pos = move_waypoint(file_name)
    return get_manhattan(boat_pos)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Number of arguments invalid.")
        print("Please provide the path of at least one valid input file")
        print("i.e. day_12.py input.txt")

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