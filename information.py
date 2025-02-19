def typeOfinstruction(cmd):
    instruction_dict = {
        "add": "R", "sub": "R", "slt": "R", "srl": "R", "or": "R", "and": "R",
        "lw": "I", "addi": "I", "jalr": "I",
        "sw": "S",
        "beq": "B", "bne": "B",
        "jal": "J"
    };
    if cmd in instruction_dict.keys():
        return instruction_dict[cmd];
    else:
        return "Instruction Not Found";

def opcode(x):
    opcode_dict={
        "r":0b0110011,
        "lw":0b0000011,
        "addi":0b0010011,
        "jalr":0b1100111,
        "sw":0b0100011,
        "beq":0b1100011,
        "bne":0b1100011,
        "jal":0b1101111
    }
    return opcode_dict[x];

def rTypeinstruction(rd,rs1,rs2,cmd):
    funct7  = 0b0000000;
    if(cmd == "sub"):
        funct7 = 0b0100000;
    funct3 = {"add":0b000,"sub":0b000,"slt":0b010,"srl":0b101,"or":0b110,"and":0b111};
    return format((funct7 << 25) | (rs2 << 20) | (rs1 << 15) | (funct3[cmd] << 12) | (rd << 7) | opcode("r"), '032b');

def iTypeinstruction(rd,rs1,imm,cmd):
    new_imm = None
    if imm>=0:
        new_imm = format((imm & (1 <<12)-1),"012b");
    else:
        new_imm = format((-imm & (1 << 12)-1),"012b");
        complement = ''.join('1' if bit == '0' else '0' for bit in imm);
        two_complement = (bin(int(complement, 2) + 1));
        new_imm = two_complement;
    
    funct3 = {"lw":0b010,"addi":0b000,"jalr":0b000};
    return format((int(new_imm,2) << 20) | (rs1 << 15) | (funct3[cmd] << 12) | (rd << 7) | opcode(cmd), '032b');

def sTypeinstruction(rs1,rs2,imm,cmd):
    new_imm = None
    if imm>=0:
        new_imm = format((imm & (1 <<12)-1),"012b");
    else:
        new_imm = format((-imm & (1 << 12)-1),"012b");
        complement = ''.join('1' if bit == '0' else '0' for bit in imm);
        two_complement = (bin(int(complement, 2) + 1));
        new_imm = two_complement;
    
    imm_left = (new_imm >> 5) & 0x7F;
    imm_right = new_imm & 0x1F;
    return format((imm_left << 25) | (rs2 << 20) | (rs1 << 15) | (0b010 << 12) | (imm_right << 7) | opcode(cmd), '032b');

def bTypeinstruction(rs1,rs2,imm,cmd):
    new_imm = None
    if imm>=0:
        new_imm = format((imm & (1 <<12)-1),"012b");
    else:
        new_imm = format((-imm & (1 << 12)-1),"012b");
        complement = ''.join('1' if bit == '0' else '0' for bit in imm);
        two_complement = (bin(int(complement, 2) + 1));
        new_imm = two_complement;
    
    funct3 = {"beq":0b000,"bne":0b001};
    new_imm = int(new_imm,2);
    imm12Bit = (new_imm >> 11) & 0x1;
    imm10To5bit = (new_imm >> 5) & 0x3F;
    imm4To1bit = (new_imm >> 1) & 0xF;
    imm11Bit = (new_imm >> 10) & 0x1;

    return format((imm12Bit << 31) | (imm10To5bit << 25) | (rs2 << 20) | (rs1 << 15) | (funct3 << 12) | (imm4To1bit << 8) | (imm11Bit << 7) | opcode(cmd), '032b');