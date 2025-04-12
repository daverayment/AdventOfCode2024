import re
# from collections import Counter
# import numpy as np

class Robot:
    def __init__(self, width, height, x, y, vx, vy):
        self.width = width
        self.height = height
        self.start_x = x
        self.start_y = y
        self.vx = vx
        self.vy = vy

    def move(self, time):
        # Move to the position at a given time.
        self.x = (self.start_x + self.vx * time) % self.width
        self.y = (self.start_y + self.vy * time) % self.height

    def get_quadrant(self, time):
        self.move(time)

        if self.x == self.width // 2 or self.y == self.height // 2:
            return None

        if self.x < self.width // 2:
            if self.y < self.height // 2:
                return 1
            else:
                return 2
        else:
            if self.y < self.height // 2:
                return 3
            else:
                return 4

# def mirror(x, width):
#     centre_x = width // 2
#     return centre_x + (centre_x - x)

def show_map(robots):
    global width, height

    for y in range(height):
        for x in range(width):
            if any(robot.x == x and robot.y == y for robot in robots):
                print('#', end='')
            else:
                print('.', end='')
        print()


width = 101
height = 103
with open('day14/input.txt', 'r') as f:
    # Convert string numbers to ints and unpack them for the robot constructor.
    robots = [Robot(width, height, *map(int, re.findall(r'-?\d+', line))) for line in f]

total = 1
for i in range(4):
    quadrant_count = sum(robot.get_quadrant(time=100) == i + 1 for robot in robots)
    total *= 1 if quadrant_count == 0 else quadrant_count

print(f'Day 14 Part 1: {total}')

# Standard Deviation answer. Slow because each time step is checked, but works. The solution is
# just the time step with the maximum standard deviation for the quadrant counts, indicating the
# Christmas tree skews the counts toward one quadrant.
#
# sd_max = (0, 0)
# for time in range(10000):
#     for robot in robots:
#         robot.move(time)

#     quadrant_results = (robot.get_quadrant(time) for robot in robots)
#     counts = Counter(quadrant_results)
#     std_dev = np.std([counts.get(i, 0) for i in range(1, 5)])
#     if std_dev > sd_max[1]:
#         sd_max = (time, std_dev)

# print(f'Day 14 Part 2: {sd_max[0]}')


# Neighbour count solutions. Works, but slow, because it checks each time step. This counts the
# robots with neighbours to their left or right.
#
#def has_neighbour(robot, positions):
# # directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
# directions = [(-1, 0), (1, 0)]
# for dx, dy in directions:
#     rx = robot.x + dx
#     ry = robot.y + dy
#     if (rx, ry) in positions:
#         return True
# return False
#
# neighbour_max = (0, 0)
# for time in range(width * height):
#     found = True
#     positions = set()
#     neighbours = 0
#     for robot in robots:
#         robot.move(time)
#         if has_neighbour(robot, positions):
#             neighbours += 1

#         positions.add((robot.x, robot.y))

#     neighbour_max = (time, neighbours) if neighbours > neighbour_max[1] else neighbour_max

# print(f'Day 14 Part 2: {neighbour_max[0]}')


# Fast solution. Just checks that no robots overlap at a given time.
for time in range(10000):
    positions = set()
    found = True
    for robot in robots:
        robot.move(time)
        if (robot.x, robot.y) in positions:
            found = False
            break
        positions.add((robot.x, robot.y))
    if found:
        break
#show_map(robots)

print(f'Day 14 Part 2: {time}')
