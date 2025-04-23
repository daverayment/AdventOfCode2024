DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

# Gets all the coordinate offsets and times which can be reached at or under the limit.
def get_offsets(limit):
    return set([
        (x, y, abs(x) + abs(y))
        for x in range(-limit, limit + 1)
        for y in range(-limit, limit + 1)
        if abs(x) + abs(y) <= limit
    ])

def do_search(track, track_positions, time_limit = 2, min_saving = 100):
    shortcut_count = 0
    offsets = get_offsets(time_limit)

    for i, (x, y) in enumerate(track):
        for dx, dy, time in offsets:
            x1, y1 = x + dx, y + dy
            track_pos = track_positions.get((x1, y1), None)
            if track_pos is not None and track_pos - i - time >= min_saving:
                shortcut_count += 1

    return shortcut_count


with open('Day 20/input.txt', 'r') as f:
    lines = [line.strip() for line in f]

for y, line in enumerate(lines):
    x = line.find('S')
    if x != -1:
        start = (x, y)

# Map out the track, including start and end.
x, y = start
track = [start]
track_positions = {start: 0}    # fast lookup for track position based on coordinate
track_len = 1
while lines[y][x] != 'E':
    for dx, dy in DIRECTIONS:
        x1, y1 = x + dx, y + dy
        if lines[y1][x1] != '#' and (x1, y1) not in track:
            track.append((x1, y1))
            track_positions[(x1, y1)] = track_len
            x, y = x1, y1
            track_len += 1
            break

shortcuts = do_search(track, track_positions, time_limit = 2)
print(f'Day 20 Part 1: {shortcuts}')

shortcuts = do_search(track, track_positions, time_limit = 20)
print(f'Day 20 Part 2: {shortcuts}')
