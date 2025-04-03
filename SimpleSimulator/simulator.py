import sys
def read_instructions_from_file(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if len(line.strip()) == 32 and set(line.strip()).issubset({'0', '1'})]

def binary_to_int(binary):
    # Convert binary string to two's complement integer
    if len(binary) == 0:
        return 0
    if binary[0] == '1':
        inverted = ''.join('1' if bit == '0' else '0' for bit in binary)
        return -(int(inverted, 2) + 1)
    else:
        return int(binary, 2)

def riscv_binary_to_registers(binary_instruction, registers, pc, datamem):
    opcode = binary_instruction[-7:]
    funct3 = binary_instruction[17:20]
    rd = int(binary_instruction[20:25], 2)
    rs1 = int(binary_instruction[12:17], 2)
    rs2 = int(binary_instruction[7:12], 2)
    imm = binary_instruction[:12]
    funct7 = binary_instruction[:7]
    new_pc = pc + 1  # Default to next instruction (index increment)

    # I-type instructions
    if opcode in ["0000011", "0010011", "1100111"]:
        imm_val = binary_to_int(imm)
        if opcode == "0000011":  # LW
            addr = registers[rs1] + imm_val
            if addr in datamem and addr % 4 == 0:
                if rd != 0:
                    registers[rd] = datamem.get(addr, 0)
        elif opcode == "1100111":  # JALR
            target_addr = (registers[rs1] + imm_val) & ~1
            new_pc = target_addr // 4
            if rd != 0:
                registers[rd] = (pc + 1) * 4  # Return address
        elif funct3 == "000":  # ADDI
            result = registers[rs1] + imm_val
            if rd != 0:
                registers[rd] = result & 0xFFFFFFFF
        elif funct3 == "011":  # SLTIU
            result = 1 if (registers[rs1] & 0xFFFFFFFF) < (imm_val & 0xFFFFFFFF) else 0
            if rd != 0:
                registers[rd] = result

    # R-type instructions
    elif opcode == "0110011":
        if funct3 == "000":
            if funct7 == "0100000":  # SUB
                result = (registers[rs1] - registers[rs2]) & 0xFFFFFFFF
            else:  # ADD
                result = (registers[rs1] + registers[rs2]) & 0xFFFFFFFF
            if rd != 0:
                registers[rd] = result
        elif funct3 == "010":  # SLT
            result = 1 if (registers[rs1] & 0xFFFFFFFF) < (registers[rs2] & 0xFFFFFFFF) else 0
            if rd != 0:
                registers[rd] = result
        elif funct3 == "101":  # SRL
            shamt = registers[rs2] & 0x1F
            result = (registers[rs1] & 0xFFFFFFFF) >> shamt
            if rd != 0:
                registers[rd] = result
        elif funct3 == "110":  # OR
            result = (registers[rs1] | registers[rs2]) & 0xFFFFFFFF
            if rd != 0:
                registers[rd] = result
        elif funct3 == "111":  # AND
            result = (registers[rs1] & registers[rs2]) & 0xFFFFFFFF
            if rd != 0:
                registers[rd] = result

    # B-type instructions
    elif opcode == "1100011":
        imm_b = binary_instruction[0] + binary_instruction[24] + binary_instruction[1:7] + binary_instruction[20:24]
        imm_val = binary_to_int(imm_b) * 2  # Byte offset
        if funct3 == "000":  # BEQ
            if registers[rs1] == registers[rs2]:
                new_pc = pc + (imm_val // 4)
        elif funct3 == "001":  # BNE
            if registers[rs1] != registers[rs2]:
                new_pc = pc + (imm_val // 4)
    # S-type instructions
    elif opcode == "0100011":  # SW
        imm_high = binary_instruction[:7]
        imm_low = binary_instruction[20:25]
        imm = imm_high + imm_low
        imm_val = binary_to_int(imm)
        addr = registers[rs1] + imm_val
        if addr % 4 == 0:
            datamem[addr] = registers[rs2] & 0xFFFFFFFF

    # J-type instructions (JAL)
    elif opcode == "1101111":
        imm_20 = binary_instruction[0]
        imm_10_1 = binary_instruction[1:11]
        imm_11 = binary_instruction[11]
        imm_19_12 = binary_instruction[12:20]
        imm = imm_20 + imm_19_12 + imm_11 + imm_10_1
        imm_val = binary_to_int(imm) * 2  # Byte offset
        new_pc = pc + (imm_val // 4)
        if rd != 0:
            registers[rd] = (pc + 1) * 4

    return registers, new_pc


def process_binary_instructions(input_file, output_file):
    # Main function to process instructions from input file and write to output file.
    try:
        binary_instructions = read_instructions_from_file(input_file)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found!")
        return

    virtual_halt = "00000000000000000000000001100011"
    registers = [0] * 32
    registers[2] = 0x17C  # Stack pointer
    pc = 0
    datamem = {0x00010000 + 4 * i: 0 for i in range(32)}

    with open(output_file, "w") as file:
        while pc < len(binary_instructions):
            current_instr = binary_instructions[pc]
            if current_instr == virtual_halt:
                break

            original_pc = pc
            registers_copy = registers.copy()
            registers, new_pc = riscv_binary_to_registers(current_instr, registers_copy, pc, datamem)
            pc = new_pc

            # Write PC after instruction execution
            current_pc_value = new_pc * 4
            file.write(f"0b{current_pc_value:032b} ")
            for reg in registers:
                file.write(f"0b{reg & 0xFFFFFFFF:032b} ")
            file.write("\n")

        # Write final state
        if pc < len(binary_instructions):
            current_pc_value = pc * 4
            file.write(f"0b{current_pc_value:032b} ")
            for reg in registers:
                file.write(f"0b{reg & 0xFFFFFFFF:032b} ")
            file.write("\n")

