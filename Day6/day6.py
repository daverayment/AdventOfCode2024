# NESW
directions = [[0,-1],[1,0],[0,1],[-1,0]]

def get_route(start, lines, test_obstacle = None) -> set:
    visited = set()
    turns = set()
    x, y = start
    direction_index = 0

    while True:
        visited.add((x, y))
        d = directions[direction_index]
        next_x, next_y = x + d[0], y + d[1]
        if next_x < 0 or next_y < 0 or next_x == len(lines[0]) or next_y == len(lines):
            return visited

        next_direction_index = (direction_index + 1) % len(directions)

        # Continue to the next cell or turn if there is an obstacle ahead.
        if lines[next_y][next_x] == '#' or (next_x, next_y) == test_obstacle:
            if ((x, y, direction_index) in turns):
                # There is a loop. We denote this by returning None.
                return None

            turns.add((x, y, direction_index))
            direction_index = next_direction_index
        else:
            x, y = next_x, next_y    

with open('day6/input.txt', 'r') as f:
    lines = [line.strip() for line in f]

for start_y, line in enumerate(lines):
    start_x = line.find('^')
    if start_x > -1:
        break

part1_route = get_route((start_x, start_y), lines)
print(f'Day 6 Part 1: {len(part1_route)}')  # 4964

looping_routes = sum(
    get_route((start_x, start_y), lines, potential_obstacle) is None
    for potential_obstacle in part1_route
)

print(f'Day 6 Part 2: {looping_routes}')    # 1740
