from itertools import product
from multiprocessing import Pool, freeze_support
from functools import partial

def process_line(line, operators):
    total = int(line[0].strip(':'))
    first = int(line[1])
    rest = line[2:]

    for ops in product(operators, repeat=len(rest)):
        current = first
        for next_num, op in zip(rest, ops):
            next_num = int(next_num)
            if op == '|':
                current = int(f'{current}{next_num}')
            elif op == '*':
                current *= next_num
            else:
                current += next_num

            if current > total:
                break

        if current == total:
            return current

    return 0 # No solution found


if __name__ == '__main__':
    freeze_support()

    with open('day7/input.txt', 'r') as f:
        lines = [line.split() for line in f]

    # We use partial instead of lambda to make the function picklable - this is required for multiprocessing.
    with Pool() as pool:
        p1 = sum(pool.map(partial(process_line, operators=['+', '*']), lines))
        print(f'Day 7 Part 1: {p1}')

        p2 = sum(pool.map(partial(process_line, operators=['+', '|', '*']), lines))
        print(f'Day 7 Part 2: {p2}')
