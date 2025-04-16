import heapq

DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
WIDTH = 71
HEIGHT = 71
INITIAL_WALL_COUNT = 1024

def manhattan_distance(node, goal):
    """Used as the h cost function to estimate distance to the goal from a node. In this puzzle,
    we could just use the sum of the node's X and Y, but this is more general."""
    return abs(goal[0] - node[0]) + abs(goal[1] - node[1])

def a_star(start, end):
    """A* pathfinding algorithm."""
    frontier = []
    heapq.heappush(frontier, (0, start))    # (priority, node)
    # The lowest cost previous node for each node.
    came_from = {}
    # The cost to reach each node from the start.
    cost_so_far = {start: 0}
    goal_found = False

    while frontier:
        current = heapq.heappop(frontier)[1]
        if current == end:
            goal_found = True
            break

        for dx, dy in DIRECTIONS:
            next_node = (current[0] + dx, current[1] + dy)
            if next_node[0] < 0 or next_node[0] > WIDTH - 1 or next_node[1] < 0 or next_node[1] > HEIGHT - 1:
                continue

            # NB: the cost is always 1 for each step, as this is a uniform grid.
            new_cost = cost_so_far[current] + 1

            # If the node is valid and the cost to reach it is the cheapest found for that location,
            # update the costs, push to the priority queue, and save the previous node.
            if next_node not in WALLS and (next_node not in cost_so_far or new_cost < cost_so_far[next_node]):
                cost_so_far[next_node] = new_cost
                priority = new_cost + manhattan_distance(next_node, end) # (we could also just use next[0] + next[1] because the goal is in the lower-right corner)
                heapq.heappush(frontier, (priority, next_node))
                came_from[next_node] = current

    return_path = reconstruct_path(came_from, start, end) if goal_found else None
    return return_path

def reconstruct_path(came_from, start, end):
    """Reconstruct the path from the end node back to the start."""
    path = set()
    current = end
    while current != start:
        path.add(current)
        current = came_from[current]
    path.add(start)
    return path


with open('Day18/input.txt', 'r') as f:
    coords = [(int(x), int(y)) for x, y in (line.split(',') for line in f.readlines())]

# Part 1. Add the first 'kilobyte' of 'corrupted data' to the map.
WALLS = {coords[i] for i in range(INITIAL_WALL_COUNT)}
start = (0, 0)
end = (WIDTH - 1, HEIGHT - 1)

return_path = a_star(start, end)
print(f'Day 18 Part 1: {len(return_path) - 1}') # -1 because the start node is included in the path.

# Part 2. Add walls/corruption until there is no valid path from the start to the end.
for _, next_wall in enumerate(coords[INITIAL_WALL_COUNT:]):
    WALLS.add(next_wall)
    if next_wall not in return_path:
        # No need to recalculate the path if the new wall is not in the way.
        continue
    return_path = a_star(start, end)
    if not return_path:
        break

print(f'Day 18 Part 2: {next_wall[0]},{next_wall[1]}')
