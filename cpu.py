"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Each index is a byte
        # RAM stores 256 bytes
        self.ram = [0] * 256

        # Each index in reg is a reg
        self.reg = [0] * 8

        # Store the Program Counter
        self.pc = 0
        self.hlt = False

        self.reg[7] = 0xF3  # stack pointer
        self.SP = 7
        self.previous = None

        #Flag pointer
        self.FP = 4
        self.Flag = self.reg[self.FP]

        self.inst = {
            HLT: self.HLT,
            LDI: self.LDI,
            MUL: self.MUL,
            PRN: self.PRN,
            POP: self.POP,
            PUSH: self.PUSH,
            CALL: self.CALL,
            RET: self.RET,
            ADD: self.ADD,
            CMP: self.CMP,
            JMP: self.JMP,
            JEQ: self.JEQ,
            JNE: self.JNE
        }

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def MUL(self, operand_a, operand_b):
        self.alu('MUL', operand_a, operand_b)

    def HLT(self, address, value):
        self.hlt = True

    def LDI(self, address, value):
        self.reg[address] = value

    def PRN(self, address, operand_b):
        print(self.reg[address])

    def POP(self, operand_a, operand_b):
        self.reg[operand_a] = self.ram[self.reg[self.SP]]
        self.ram[self.reg[self.SP]] = 0
        self.reg[self.SP] += 1

    def PUSH(self, operand_a, operand_b):
        self.reg[self.SP] -= 1
        self.ram[self.reg[self.SP]] = self.reg[operand_a]

    def CALL(self, operand_a, operand_b):
        self.previous = self.pc + 2
        self.pc = self.reg[operand_a]

    def RET(self, operand_a, operand_b):    
        self.pc = self.previous
        self.prevous = None

    def ADD(self, operand_a, operand_b):
        self.alu("ADD", operand_a, operand_b)

    def CMP(self, operand_a, operand_b):
        self.alu("CMP", operand_a, operand_b)

    def JMP(self, operand_a, operand_b):
        self.pc = self.reg[operand_a]

    def JEQ(self, operand_a, operand_b):
        # if equal flag is true then jump to address stored in given register.
        if self.Flag == 0b00000001:
            self.pc = self.reg[operand_a]
        else:
        # else if equal falg is false increase PC by 2
            self.pc += 2

    def JNE(self, operand_a, operand_b):
        # if equal flag is false or clear then jump to address stored in given register.
        if self.Flag == 0b00000100 or self.Flag == 0b00000010:
            self.pc = self.reg[operand_a]
        else:
        # else if flag is true increase PC by 2
            self.pc += 2

    def load(self, filename):
        """Load a program into memory."""
        address = 0

        with open(filename) as f:
            # for each line in the file
            for line in f:
                comment_split = line.split('#')
                instruction = comment_split[0]

                if instruction == '':
                    continue

                first_bit = instruction[0]
                if first_bit == "0" or first_bit == "1":
                    self.ram[address] = int(instruction[:8], 2)
                    address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op =="CMP":
            # Compare the values in two registers.
            # `FL` bits: `00000LGE`
            if self.reg[reg_a] < self.reg[reg_b]:
            # * If reg_a is less than reg_b, set the Less-than flag to 1,
            #   otherwise set it to 0.
                self.Flag = 0b00000100

            elif self.reg[reg_a] == self.reg[reg_b]:
            # * If they are equal, set the Equal flag to 1, otherwise set it to 0.
                self.Flag = 0b00000001

            elif self.reg[reg_a] > self.reg[reg_b]:
            # * If reg_a is greater than reg_b, set the Greater-than flag
            #   to 1, otherwise set it to 0.
                self.Flag = 0b00000010

            else:
                print('Code is broken')

        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f'TRACE: %02X | %02X %02X %02X |' % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(' %02X' % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        while not self.hlt:
            IR = self.ram[self.pc]

            # Using `ram_read()`,read the bytes at `PC+1` and `PC+2` from RAM into variables
            # `operand_a` and `operand_b` in case the instruction needs them.
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # Then, depending on the value of the opcode, perform the actions needed for the
            # instruction per the LS-8 spec.
            # if IR == HLT:
            #    running = False
            # elif IR == LDI:
            #    self.reg[operand_a] = operand_b
            #    self.pc += 3
            # elif IR == PRN:
            #    print(self.reg[operand_a])
            #    self.pc += 2
            # elif IR == MUL:
            #    self.alu("MUL", operand_a, operand_b)
            #    self.pc += 3
            # else:
            #   print("Unknown instruction.")
            op_size = IR >> 6
            ins_set = ((IR >> 4) & 0b1) == 1

            if IR in self.inst:
                self.inst[IR](operand_a, operand_b)

            if not ins_set:
                self.pc += op_size + 1