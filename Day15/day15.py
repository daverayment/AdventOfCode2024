class Floor:
    DIRECTIONS = {'^': (0, -1), 'v': (0, 1), '<': (-1, 0), '>': (1, 0)}

    def clear(self):
        self.objects = {}
        self.robot_pos = None
        
    def read_line(self, line, y, is_part_two=False):
        for x, ch in enumerate(line):
            x_pos = x * 2 if is_part_two else x
            if ch != '.':
                self.objects[(x_pos, y)] = ch
                if ch == '@':
                    self.robot_pos = (x_pos, y)
                    
                if is_part_two:
                    if ch == 'O':
                        # Wider boxes.
                        self.objects[(x_pos, y)] = '['
                        self.objects[(x_pos + 1, y)] = ']'
                    elif ch == '#':
                        # Double-walls
                        self.objects[(x_pos + 1, y)] = ch

    def do_moves(self, instructions):
        for move in instructions:
            #self.show()
            dx, dy = self.DIRECTIONS[move]
            #print('\nMove: ', move, 'dx:', dx, 'dy:', dy)
            moves = self.get_moves([self.robot_pos], dx, dy)
            self.execute_moves(moves)

    def get_moves(self, to_visit, dx, dy):
        moves = []
        visited = set()
        while to_visit:
            pos = to_visit.pop()
            if pos in visited:
                continue
            visited.add(pos)
            if pos in self.objects:
                ch = self.objects[pos]
                if ch == '#':
                    moves = []
                    break
                new_pos = (pos[0] + dx, pos[1] + dy)
                moves.append((ch, pos, new_pos))
                if ch == '[':
                    to_visit.append((pos[0] + 1, pos[1]))
                if ch == ']':
                    to_visit.append((pos[0] - 1, pos[1]))
                to_visit.append(new_pos)
        return moves
    
    def execute_moves(self, moves):
        for move in moves:
            del self.objects[move[1]]

        while moves:
            move = moves.pop()
            self.objects[move[2]] = move[0]
            if move[0] == '@':
                self.robot_pos = move[2]

    def show(self):
        max_x = max(x for x, _ in self.objects.keys())
        max_y = max(y for _, y in self.objects.keys())
        
        for y in range(max_y + 1):
            line = ''
            for x in range(max_x + 1):
                if (x, y) == self.robot_pos:
                    line += '@'
                elif (x, y) in self.objects:
                    line += self.objects[(x, y)]
                else:
                    line += '.'
            print(line)

    def do_part(self, map_lines, instr, is_part_two=False):
        self.clear()
        for y, line in enumerate(map_lines):
            floor.read_line(line, y, is_part_two)
        floor.do_moves(instr)
        floor.show()

        score = sum(pos[1] * 100 + pos[0] for pos, value in self.objects.items() if (value == 'O' or value == '['))
        print(f'Day 15 Part {"2" if is_part_two else "1"}: {score}')


in_map = True
map_lines = []
floor = Floor() 
instr = ''

with open('Day15/input.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if line == '':
            in_map = False
        if in_map:
            map_lines.append(line)
        else:
            instr += line

floor.do_part(map_lines, instr)
floor.do_part(map_lines, instr, is_part_two=True)
