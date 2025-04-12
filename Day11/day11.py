import functools

def do_part(stones, blinks, part_num):
    total = sum(get_length(stone, blinks) for stone in stones)
    print(f'Day 11 Part {part_num}: {total}')

@functools.cache
def get_length(stone, blinks_remaining):
    if blinks_remaining == 0:
        return 1
    
    # Normalise numbers with leading zeroes.
    stone = str(int(stone))

    if stone == '0':
        return get_length('1', blinks_remaining - 1)
    elif len(stone) % 2 == 0:
        half = int(len(stone) / 2)
        return get_length(stone[:half], blinks_remaining - 1) + get_length(stone[half:], blinks_remaining - 1)
    else:
        return get_length(str(int(stone) * 2024), blinks_remaining - 1)


with open('Day11/input.txt', 'r') as f:
    stones = f.readline().split()

for blinks, part_num in [(25, 1), (75, 2)]:
    do_part(stones, blinks, part_num)
