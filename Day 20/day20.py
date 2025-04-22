DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def do_search(track, time_limit = 2, min_saving = 100):
    shortcuts = []
    track_len = len(track)
    
    for i, (x, y) in enumerate(track):
        for j in range(i + min_saving, track_len):
            x1, y1 = track[j]
            shortcut_time = abs(x - x1) + abs(y - y1)
            saving = j - i - shortcut_time
            if shortcut_time <= time_limit and saving >= min_saving:
                shortcuts.append(((x, y), (x1, y1), saving))

    return shortcuts


with open('Day 20/input.txt', 'r') as f:
    lines = [line.strip() for line in f]

for y, line in enumerate(lines):
    x = line.find('S')
    if x != -1:
        start = (x, y)

# Map out the track, including start and end.
x, y = start
track = [start]
while lines[y][x] != 'E':
    for dx, dy in DIRECTIONS:
        x1, y1 = x + dx, y + dy
        if lines[y1][x1] != '#' and (x1, y1) not in track:
            track.append((x1, y1))
            x, y = x1, y1
            break

shortcuts = do_search(track, time_limit = 2, min_saving = 100)
print(f'Day 20 Part 1: {len(shortcuts)}')

shortcuts = do_search(track, time_limit = 20)
print(f'Day 20 Part 2: {len(shortcuts)}')
