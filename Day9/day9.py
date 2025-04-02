def make_disk_map(line):
    disk = []
    files = {}
    file_id = 0
    i = 0
    file_pos = 0
    map_len = len(line)

    while i < map_len:
        file_len = int(line[i])
        disk.extend([file_id] * file_len)
        files[file_id] = (file_pos, file_len)
        file_pos += file_len
        if i < map_len - 1:
            spaces = int(line[i + 1])
            disk.extend(['.'] * spaces)
            file_pos += spaces
        i += 2
        file_id += 1
    return disk, files

def checksum(disk):
    return sum(i * num for i, num in enumerate(disk) if num != '.')

with open('Day9/input.txt', 'r') as f:
    line = f.readline()

# Part 1
disk, _ = make_disk_map(line)

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

print(f'Day 9 Part 1: {checksum(disk)}')

# Part 2
def get_contiguous_space(disk, file_start, file_len):
    for i in range(file_start):
        if disk[i] == '.':
            found = True
            for j in range(1, file_len):
                if disk[i + j] != '.':
                    found = False
                    break
            if found:
                return i
    return None

def insert_file(disk, insert_start, file_start, file_len):
    # Use slices to copy the file and blank out where it was.
    disk[insert_start : insert_start + file_len] = \
        disk[file_start : file_start + file_len]
    disk[file_start : file_start + file_len] = ['.'] * file_len

# Recreate the disk layout.
disk, files = make_disk_map(line)
# Last file id.
file_id = len(line) // 2

while file_id > 0:
    file_start, file_len = files[file_id]

    # Search for contiguous space to fit file. One attempt per file only.
    if (start := get_contiguous_space(disk, file_start, file_len)) != None and start < file_start:
        insert_file(disk, start, file_start, file_len)

    file_id -= 1

print(f'Day 9 Part 2: {checksum(disk)}')
