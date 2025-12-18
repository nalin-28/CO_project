# 💻 RISC-V Assembler & Simulator

A complete implementation of a custom **Assembler** and **Simulator** for the **RV32I (RISC-V 32-bit integer)** instruction set, demonstrating the full pipeline from assembly language to binary execution.

**Course:** Computer Organization (CSE112) | **Instructor:** Prof. Sujay Deb  
**Tech Stack:** Python, RISC-V ISA, Assembly Language

---

## 🛠️ Components

### SimpleAssembler
Translates RISC-V assembly code into 32-bit binary machine code with comprehensive error detection.

**Features:**
- Supports R, I, S, B, J-type instruction formats
- Label resolution for branches and jumps
- Detects syntax errors, invalid registers, and out-of-bounds immediates
- Ensures proper Virtual Halt instruction placement

### SimpleSimulator
Executes binary machine code and generates detailed execution traces.

**Features:**
- Interprets and executes RISC-V binary instructions
- Tracks Program Counter and all 32 registers after each instruction
- Manages program, stack, and data memory (512 bytes total)
- Outputs final memory state upon program termination

---

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/tanish-j12/CO_project.git
cd CO_project

# Assemble: Convert assembly to binary
python3 SimpleAssembler/assembler.py input.asm output.bin

# Simulate: Execute binary and generate trace
python3 SimpleSimulator/simulator.py output.bin trace.txt
```

---

## 📝 Example Usage

**Assembly Code (sample.asm):**
```assembly
addi sp, zero, 380       # Initialize stack pointer
addi t0, zero, 10        # Load constant
addi t1, zero, 20        # Load constant
add t2, t0, t1           # Add: t2 = t0 + t1
beq zero, zero, 0        # Virtual Halt
```

**Execution:**
```bash
python3 SimpleAssembler/assembler.py sample.asm sample.bin
python3 SimpleSimulator/simulator.py sample.bin trace.txt
```

---

## 🎯 Technical Details

### Supported Instructions
- **R-type:** `add`, `sub`, `slt`, `srl`, `or`, `and`
- **I-type:** `lw`, `addi`, `jalr`
- **S-type:** `sw`
- **B-type:** `beq`, `bne`, `blt`
- **J-type:** `jal`

### Memory Layout
| Memory Type | Address Range | Size |
|-------------|---------------|------|
| Program | `0x00000000` - `0x000000FF` | 256 bytes |
| Stack | `0x00000100` - `0x0000017F` | 128 bytes |
| Data | `0x00010000` - `0x0001007F` | 128 bytes |

### Register File
32 general-purpose registers (x0-x31) following RISC-V ABI naming convention (zero, ra, sp, t0-t6, s0-s11, a0-a7).

---

## 📊 Key Features

✅ Complete ISA implementation for RV32I subset  
✅ Two-pass assembler with label resolution  
✅ Comprehensive error detection and reporting  
✅ Cycle-accurate simulation with state tracking  
✅ Binary instruction encoding and decoding  
✅ Memory management with distinct regions

---

## 🔧 Implementation Highlights

- **Binary Encoding:** Direct handling of RISC-V instruction formats
- **Label Processing:** Automatic conversion to relative addresses
- **Error Handling:** Validates instruction syntax, register names, and immediate bounds
- **State Tracking:** Outputs PC and register values after each instruction execution
- **Memory Dump:** Final memory state visualization upon program termination

---

## 📚 What I Learned

- Computer architecture and RISC-V ISA design principles
- Assembly language programming and instruction encoding
- Building a two-pass assembler with symbol table management
- Implementing instruction decode and execution logic
- Memory organization and address space management

---

## 📄 License

This project is for **educational purposes only**.

---

## 📧 Contact

**Tanish Jindal** | CSE + Applied Math | IIIT Delhi  
📧 tanish24579@iiitd.ac.in | 💼 [LinkedIn]((https://www.linkedin.com/in/tanish-jindal-a21104344/)) | 🐙 [GitHub](https://github.com/tanish-j12)

---

⭐ **Star this repository if you find it useful!**
