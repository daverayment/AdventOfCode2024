import sys
import heapq    # used as priority queue for Dijkstra's algorithm

deltas = {'E': (1, 0), 'W': (-1, 0), 'N': (0, -1), 'S': (0, 1)}
turns = {'E': ['N', 'S'], 'W': ['N', 'S'], 'N': ['W', 'E'], 'S': ['W', 'E']}

def get_options(pos, direction, lines):
    x, y = get_new_pos(pos, direction)
    if lines[y][x] != '#':
        yield ((x, y), direction, 1)
    for new_direction in turns[direction]:
        x, y = get_new_pos(pos, new_direction)
        if lines[y][x] != '#':
            yield ((x, y), new_direction, 1001)

def get_new_pos(pos, direction):
    dx, dy = deltas[direction]
    x1, y1 = pos[0] + dx, pos[1] + dy
    return (x1, y1)

with open('Day16/input.txt', 'r') as f:
    lines = [line.strip() for line in f]

# Important notes:
# - The map has a border on all sides, so we don't do bounds checking.
# - The start direction is East.
# - The end node is at a dead-end and the last movement is eastward.
# We use the above to simplify some of the logic.
start_pos = (1, len(lines) - 2)
end_pos = (len(lines[0]) - 2, 1)

# Use Dijkstra's algorithm to find the minimum cost to reach the end.
min_score = sys.maxsize
# Stores the minimum cost for reaching a position and direction.
min_cost_for_state = {}
# Stores the previous position(s) for each optimal state. Used when backtracking in Part 2.
prev_pos_for_state = {}
prev_pos_for_state[(start_pos, 'E')] = []
pri_queue = [(0, start_pos, 'E')]   # initial state (score, position, direction)

while pri_queue:
    score, pos, direction = heapq.heappop(pri_queue)

    # If we've reached this state before with a smaller cost, skip.
    # NB: using get with a default value for when the key doesn't exist.
    if min_cost_for_state.get((pos, direction), sys.maxsize) < score:
        continue

    # If we've reached the end, this guarantees the minimum score.
    if pos == end_pos:
        min_score = min(min_score, score)
        # If we don't care about the route, we could stop here. This would be OK for part 1, but
        # part 2 requires all shortest routes to be mapped.
        #break

    for next_pos, next_direction, move_cost in get_options(pos, direction, lines):
        new_score = score + move_cost

        current_min_score = min_cost_for_state.get((next_pos, next_direction), sys.maxsize)
        if current_min_score == new_score:
            prev_pos_for_state[(next_pos, next_direction)].append((pos, direction))
        elif new_score <current_min_score:
            # The path to (next_pos, next_direction) is at a lower or equal than any previous path to this state.
            min_cost_for_state[(next_pos, next_direction)] = new_score
            prev_pos_for_state[(next_pos, next_direction)] = [(pos, direction)]
            # Add the new state to the priority queue.
            heapq.heappush(pri_queue, (new_score, next_pos, next_direction))

print(f'Day 16 Part 1: {min_score}')

# Count the positions taken up by all the optimal cost routes. We have already saved the prior
# state(s) for each minimal cost state, so simply trace these back from the end to the start.
to_visit = [(end_pos, 'E')]
visited = set()
while to_visit:
    state = to_visit.pop()
    if state in visited:
        continue
    visited.add(state)
    to_visit.extend(prev_pos_for_state[state])
# Now extract the unique positions from all the visited states to get the solution.
route_len = len({p for p, _ in visited})

print(f'Day 16 Part 2: {route_len}')
