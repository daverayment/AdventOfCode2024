from itertools import groupby

with open('Day9/input.txt', 'r') as f:
    line = f.readline()

def make_disk_map(line):
    disk = []
    file_id = 0
    i = 0
    map_len = len(line)

    while i < map_len:
        file_len = int(line[i])
        disk.extend([file_id] * file_len)
        if i < map_len - 1:
            spaces = int(line[i + 1])
            disk.extend(['.'] * spaces)
        i += 2
        file_id += 1
    return disk

# Part 1
disk = make_disk_map(line)

# Move files.
last_file_index = len(disk) - 1
i = -1

# Moves can create new spaces between existing files, so this requires multiple passes to compact
# all files.
while True:
    i = disk.index('.', i + 1)
    while disk[last_file_index] == '.':
        last_file_index -= 1

    if i >= last_file_index:
        break

    disk[i] = disk[last_file_index]
    disk[last_file_index] = '.'
    last_file_index -= 1

# Calculate checksum.
checksum = sum(i * num for i, num in enumerate(disk) if num != '.')
print(f'Day 9 Part 1: {checksum}')

# Part 2
def get_contiguous_space(disk, min_len):
    for key, group in groupby(enumerate(disk), lambda x: x[1] == '.'):
        if key:
            group_list = list(group)
            if len(group_list) >= min_len:
                return group_list[0][0]
    return None

def insert_file(disk, insert_start, delete_start, file_len, file_id):
    for i in range(insert_start, insert_start + file_len):
        disk[i] = file_id
    for i in range(delete_start, delete_start + file_len):
        disk[i] = '.'

# Recreate the disk layout.
disk = make_disk_map(line)
# Last file id.
file_id = len(line) // 2

while file_id > 0:
    file_len = disk.count(file_id)
    file_start = disk.index(file_id)

    # Search for contiguous space to fit file. One attempt per file only.
    if (start := get_contiguous_space(disk, file_len)) != None and start < file_start:
        insert_file(disk, start, file_start, file_len, file_id)

    file_id -= 1

checksum = sum(i * num for i, num in enumerate(disk) if num != '.')
print(f'Day 9 Part 2: {checksum}')