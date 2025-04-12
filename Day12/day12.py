from collections import deque

directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def calculate_region(start, lines, visited, width, height):
    if start in visited:
        return 0, 0, 0
    
    q = deque([start])
    visited.add(start)
    region = {start}

    perimeter = 0
    letter = lines[start[1]][start[0]]

    while q:
        pos = q.popleft()

        for dx, dy in directions:
            x1, y1 = pos[0] + dx, pos[1] + dy

            if (x1 < 0 or y1 < 0 or x1 >= width or y1 >= height or lines[y1][x1] != letter):
                perimeter += 1
            elif (x1, y1) not in visited:
                visited.add((x1, y1))
                region.add((x1, y1))
                q.append((x1, y1))

    min_x = min(x for x, y in region)
    min_y = min(y for x, y in region)
    max_x = max(x for x, y in region)
    max_y = max(y for x, y in region)

    # Loop through vertices from top-left to bottom-right.
    # Top-left vertex has the first cell to its bottom-right.
    fences = 0
    for vy in range(min_y, max_y + 2):
        for vx in range(min_x, max_x + 2):
            tl_in = (vx - 1, vy - 1) in region
            tr_in = (vx, vy - 1) in region
            bl_in = (vx - 1, vy) in region
            br_in = (vx, vy) in region

            count_in_region = sum([tl_in, tr_in, bl_in, br_in])
            if count_in_region == 1 or count_in_region == 3:
                # Each corner detected requires a new fence section.
                fences += 1
            elif count_in_region == 2 and \
                ((tl_in and br_in) or (tr_in and bl_in)):
                # Take into account the checkerboard pattern where two neighbouring regions
                # meet around the same vertex.
                fences += 2

    return len(region), perimeter, fences


with open('Day12/input.txt', 'r') as f:
    lines = [line.strip() for line in f]

height = len(lines)
width = len(lines[0])
visited = set()
total1 = 0
total2 = 0

for y in range(height):
    for x in range(width):
        area, perimeter, fences = calculate_region((x, y), lines, visited, width, height)
        total1 += area * perimeter
        total2 += area * fences

print(f'Day 12 Part 1: {total1}')
print(f'Day 12 Part 2: {total2}')
