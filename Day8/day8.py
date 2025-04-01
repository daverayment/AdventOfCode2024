from itertools import combinations

def read_line(line, line_num, antenna_map):
    for index, char in enumerate(line):
        if char.isalnum():
            # Add (x, y) coord to the map.
            if char in antenna_map:
                antenna_map[char].append((index, line_num))
            else:
                antenna_map[char] = [(index, line_num)]

def place_antinodes(pos, dx, dy, antinode_map, line_length, num_lines, is_part1 = True):
    if not is_part1 and pos not in antinode_map:
        antinode_map.append(pos)

    while (True):
        pos = (pos[0] + dx, pos[1] + dy)
        if pos[0] < 0 or pos[1] < 0 or pos[0] >= line_length or pos[1] >= num_lines:
            return
        
        if pos not in antinode_map:
            antinode_map.append(pos)

        # We only attempt to add a single antinode in each direction for part 1.
        if is_part1:
            return

with open('day8/input.txt', 'r') as f:
    lines = [line.rstrip('\n') for line in f]

# First build a map of all antennae.
antenna_map = {}
for line_num, line in enumerate(lines):
    read_line(line, line_num, antenna_map)

def do_part(is_part1 = True):
    antinodes = []
    num_lines = len(lines)
    line_length = len(lines[0])

    for _, positions in antenna_map.items():
        for a1, a2 in combinations(positions, 2):
            # Calculate where to place antinodes...
            # a1 will always be to the left and will never be below a2.
            dx = a2[0] - a1[0]
            dy = a2[1] - a1[1]

            place_antinodes(a1, -dx, -dy, antinodes, line_length, num_lines, is_part1)
            place_antinodes(a2, dx, dy, antinodes, line_length, num_lines, is_part1)

    return len(antinodes)

print(f'Day 8 Part 1: {do_part()}')
print(f'Day 8 Part 2: {do_part(is_part1=False)}')
