import re, sys

with open('Day13/input.txt', 'r') as f:
    lines = [line.strip() for line in f]

# Brute-force solution. I'm sure this will totally work for Part 2.
# ...oh...no.
def find_combo_bf(ax, ay, bx, by, px, py):
    best = sys.maxsize

    found = False
    for b_count in range(100, -1, -1):
        for a_count in range(100, -1, -1):
            if (a_count * ax + b_count * bx == px) and \
                (a_count * ay + b_count * by == py):
                found = True
                best = min(best, a_count * 3 + b_count)

    return found, best

def find_combo(ax, ay, bx, by, px, py):
    # Two Diophantine equations (ax + by = c) must be satisfied:
    #   a_count * ax + b_count * bx = px
    #   a_count * ay + b_count * by = py
    #
    # Make the b-terms the same. First scale by by or bx:
    #   a_count * ax * by + b_count * bx * by = px * by
    #   a_count * ay * bx + b_count * by * bx = py * bx
    #
    # Cancel out the b-terms by subtracting the second equation from the first:
    #   (a_count * ax * by + b_count * bx * by) - (a_count * ay * bx + b_count * by * bx) = px * by - py * bx
    #
    #   (a_count * ax * by) - (a_count * ay * bx) = px * by - py * bx
    #
    # Factor out a_count:
    #   a_count * (ax * by - ay * bx) = px * by - py * bx
    #
    #   a_count = (px * by - py * bx) / (ax * by - ay * bx)
    #

    a_count = (px * by - py * bx) / (ax * by - ay * bx)

    # Now b_count. Scale by ay or ax:
    #   a_count * ax * ay + b_count * bx * ay = px * ay
    #   a_count * ay * ax + b_count * by * ax = py * ax
    #
    # Cancel out the a-terms by subtracting:
    #   (a_count * ax * ay + b_count * bx * ay) - (a_count * ay * ax + b_count * by * ax) = px * ay - py * ax
    #
    #   (b_count * bx * ay) - (b_count * by * ax) = px * ay - py * ax
    #
    # Factor out b_count:
    #   b_count * (bx * ay - by * ax) = px * ay - py * ax
    #
    #   b_count = (px * ay - py * ax) / (bx * ay - by * ax)
    #

    b_count = (px * ay - py * ax) / (bx * ay - by * ax)

    # To be valid, both a_count and b_count must be integers.
    found = (a_count == int(a_count) and b_count == int(b_count))

    return found, int(a_count) * 3 + int(b_count)

total = 0
total2 = 0
i = 0
while i < len(lines):
    # Read Button A values, Button B values and the Prize location.
    ax, ay = map(int, re.findall(r'\d+', lines[i]))
    bx, by = map(int,re.findall(r'\d+', lines[i + 1]))
    px, py = map(int, re.findall(r'\d+', lines[i + 2]))
    i += 4

    found, best = find_combo(ax, ay, bx, by, px, py)
    if found:
        total += best

    found, best = find_combo(ax, ay, bx, by, px + 10000000000000, py + 10000000000000)
    if found:
        total2 += best

print(f'Day 13 Part 1: {int(total)}')
print(f'Day 13 Part 2: {int(total2)}')
