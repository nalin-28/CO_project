from information import *

rg_nums =  {
    "zero": 0b00000, "ra": 0b00001, "sp": 0b00010, "gp": 0b00011, "tp": 0b00100,
    "t0": 0b00101, "t1": 0b00110, "t2": 0b00111, "s0": 0b01000, "fp": 0b01000,
    "s1": 0b01001, "a0": 0b01010, "a1": 0b01011, "a2": 0b01100, "a3": 0b01101,
    "a4": 0b01110, "a5": 0b01111, "a6": 0b10000, "a7": 0b10001, "s2": 0b10010,
    "s3": 0b10011, "s4": 0b10100, "s5": 0b10101, "s6": 0b10110, "s7": 0b10111,
    "s8": 0b11000, "s9": 0b11001, "s10": 0b11010, "s11": 0b11011, "t3": 0b11100,
    "t4": 0b11101, "t5": 0b11110, "t6": 0b11111}

def assembly(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        contents = file.readlines()
    contents_p = [line for line in contents]
    contents_p = [line.strip() for line in contents_p]
    list_contents = []
    labels = []
    if("beq zero,zero,0") not in contents_p:
        print("Virtual Halt not found in the in the instructions")
        return
    
    for i in range(len(contents_p)):
        if ":" in contents_p[i]:
            label_,extra= contents_p[i].split(": ")
            labels.append((label_,i))

    for line in contents_p:
        inst_vars = line.strip().split()
        if ":" in inst_vars[0]:
            instruction = inst_vars[1]
            if typeOfinstruction(instruction)=="R":
                inst_vars_1 = inst_vars[2].split(',')
                rd = rg_nums[inst_vars_1[0]]
                rs1 = rg_nums[inst_vars_1[1]]
                rs2 = rg_nums[inst_vars_1[2]]
                if(inst_vars_1[0] not in rg_nums.keys() or inst_vars_1[1] not in rg_nums.keys() or inst_vars_1[2] not in rg_nums.keys()):
                    print("Resistor Naming is not correct")
                    return
                list_contents.append(rTypeinstruction(rd, rs1, rs2, instruction))

            elif typeOfinstruction(instruction)=="S":
                inst_vars_1 = inst_vars[2].split(',')
                rs2 = rg_nums[inst_vars_1[0]]
                imm_rs1 = inst_vars_1[1]
                imm = int(imm_rs1[:imm_rs1.find('(')])
                rs1 = rg_nums[imm_rs1[imm_rs1.find('(')+1:-1]]
                if(inst_vars_1[0] not in rg_nums.keys() or rs1 not in rg_nums.values()):
                    print("Resistor Naming is Not Correct")
                    return
                list_contents.append(sTypeinstruction(rs1, rs2, imm,instruction))

            elif typeOfinstruction(instruction)=="I":
                inst_vars_1 = inst_vars[2].split(',')
                rd = rg_nums[inst_vars_1[0]]
                if instruction == "lw":
                    imm_rs1 = inst_vars_1[1]
                    imm = int(imm_rs1[:imm_rs1.find('(')])
                    rs1 = rg_nums[imm_rs1[imm_rs1.find('(')+1:-1]]
                    if(inst_vars_1[0] not in rg_nums.keys() or rs1 not in rg_nums.values()):
                        print("Resistor Naming is not correct")
                        return
                else:
                    rs1 = rg_nums[inst_vars_1[1]]
                    imm = int(inst_vars_1[2])
                    if(inst_vars_1[0] not in rg_nums.keys() or inst_vars_1[1] not in rg_nums.keys()):
                        print("Resistor Naming is not correct")
                        return
                list_contents.append(iTypeinstruction(rd, rs1, imm, instruction))