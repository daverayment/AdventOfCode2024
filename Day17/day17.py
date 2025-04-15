import re

class Computer:
    def __init__(self, input):
        self.reg_a, self.reg_b, self.reg_c, *self.program = [int(a) for a in re.findall(r'\d+', input)]
        self.program_len = len(self.program)
        self.halted = False
        self.output = []

    def get_combo(self, pc):
        val = self.program[pc]
        if val < 4:
            return val
        elif val == 4:
            return self.reg_a
        elif val == 5:
            return self.reg_b
        elif val == 6:
            return self.reg_c
        else:
            raise Exception(f'Invalid operand: {val}')

    def run(self):
        self.pc = 0
        while not self.halted:
            self.step()

    def div(self):
        return self.reg_a // (2 ** self.get_combo(self.pc + 1))

    def step(self):
        if self.pc >= self.program_len:
            self.halted = True
            return

        opcode = self.program[self.pc]
        if opcode == 0:
            # adv - division of register A by combo, store result in A
            self.reg_a = self.div()
        elif opcode == 1:
            # bxl - XOR register B with literal value
            self.reg_b ^= self.program[self.pc + 1]
        elif opcode == 2:
            # bst - write combo mod 8 to register B
            self.reg_b = self.get_combo(self.pc + 1) % 8
        elif opcode == 3:
            # jnz - jump if register A is not 0
            if self.reg_a != 0:
                self.pc = self.program[self.pc + 1]
                return
        elif opcode == 4:
            # bxc - bitwise XOR register B with register C and store in B
            self.reg_b ^= self.reg_c
        elif opcode == 5:
            # out - output combo
            operand = self.get_combo(self.pc + 1) % 8
            self.output.append(operand)
        elif opcode == 6:
            # bdv - division of register A by combo, store result in B
            self.reg_b = self.div()
        elif opcode == 7:
            # cdv - division of register A by combo, store result in C
            self.reg_c = self.div()

        self.pc += 2

with open('Day17/input.txt', 'r') as f:
    computer = Computer(f.read())

computer.run()
output = ','.join(map(str, computer.output))
print(f'Day 17 Part 1: {output}')

# Part 2
def do_loop(candidate_a):
    """Simulates a single loop through the program code returning the value which would be output."""
    b = candidate_a % 8
    b ^= 5
    c = candidate_a // (2 ** b)
    b ^= 6
    b ^= c
    # NB: each iteration through the real program, the a value is shifted right by 3 bits.
    return b % 8


# Start with the end state of the program run - A will always have the value 0.
possible_a = {0}

# Loop through the program code - the desired output - in reverse. The iteration must produce the
# target octet.
for target_octet in reversed(computer.program):
    candidates = set()

    for a in possible_a:
        # Try all possible 3-bit values mixed with shifted candidates.
        for lower_bits in range(8):
            # Reconstruct the pre-shifted A value.
            test_a = (a << 3) | lower_bits
            # Add to the set if the desired output is produced.
            if do_loop(test_a) == target_octet:
                candidates.add(test_a)

    # Update the set of possible A values. Each of these will produce the target octet and all
    # subsequent code.
    possible_a = candidates

print(f'Day 17 Part 2: {min(possible_a)}')
