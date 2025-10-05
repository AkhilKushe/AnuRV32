import cocotb
from cocotb.triggers import RisingEdge
from cocotb.coverage import CoverPoint

# --- RV32I instruction table ---
# (name, opcode, funct3, funct7) ; use None for unused fields
instr_table = [
    # R-type
    ("ADD",  0b0110011, 0b000, 0b0000000),
    ("SUB",  0b0110011, 0b000, 0b0100000),
    ("SLL",  0b0110011, 0b001, 0b0000000),
    ("SLT",  0b0110011, 0b010, 0b0000000),
    ("SLTU", 0b0110011, 0b011, 0b0000000),
    ("XOR",  0b0110011, 0b100, 0b0000000),
    ("SRL",  0b0110011, 0b101, 0b0000000),
    ("SRA",  0b0110011, 0b101, 0b0100000),
    ("OR",   0b0110011, 0b110, 0b0000000),
    ("AND",  0b0110011, 0b111, 0b0000000),

    # I-type arithmetic/logical
    ("ADDI", 0b0010011, 0b000, None),
    ("SLTI", 0b0010011, 0b010, None),
    ("SLTIU",0b0010011, 0b011, None),
    ("XORI", 0b0010011, 0b100, None),
    ("ORI",  0b0010011, 0b110, None),
    ("ANDI", 0b0010011, 0b111, None),
    ("SLLI", 0b0010011, 0b001, 0b0000000),
    ("SRLI", 0b0010011, 0b101, 0b0000000),
    ("SRAI", 0b0010011, 0b101, 0b0100000),

    # Load (I-type memory)
    ("LB",   0b0000011, 0b000, None),
    ("LH",   0b0000011, 0b001, None),
    ("LW",   0b0000011, 0b010, None),
    ("LBU",  0b0000011, 0b100, None),
    ("LHU",  0b0000011, 0b101, None),

    # Store (S-type)
    ("SB",   0b0100011, 0b000, None),
    ("SH",   0b0100011, 0b001, None),
    ("SW",   0b0100011, 0b010, None),

    # Branch (B-type)
    ("BEQ",  0b1100011, 0b000, None),
    ("BNE",  0b1100011, 0b001, None),
    ("BLT",  0b1100011, 0b100, None),
    ("BGE",  0b1100011, 0b101, None),
    ("BLTU", 0b1100011, 0b110, None),
    ("BGEU", 0b1100011, 0b111, None),

    # U-type
    ("LUI",  0b0110111, None, None),
    ("AUIPC",0b0010111, None, None),

    # J-type
    ("JAL",  0b1101111, None, None),

    # I-type JALR
    ("JALR", 0b1100111, 0b000, None),
]

# --- Cocotb Test ---
@cocotb.test()
async def rv32i_functional_coverage(dut):
    while True:
        await RisingEdge(dut.clk)
        if not dut.instr_valid.value:
            continue

        instr = int(dut.instr.value)
        opcode = instr & 0x7f
        funct3 = (instr >> 12) & 0x7
        funct7 = (instr >> 25) & 0x7f

        # Sample correct instruction bin
        for name, op, f3, f7 in instr_table:
            if opcode == op and (f3 is None or funct3 == f3) and (f7 is None or funct7 == f7):
                CoverPoint(name, bins=[1]).sample()
                break
