import cocotb
from cocotb.triggers import FallingEdge, Timer, RisingEdge, Edge, Event
from cocotb.clock import Clock
import cocotb_coverage.coverage
from riscvmodel.insn import *
from riscvmodel.regnames import *
from riscvmodel.variant import RV32I
from riscvmodel.model import Model
from riscvmodel.code import decode
import random
from MemoryModel import MemoryModel
from cocotb_coverage.coverage import *

out_instr = open("instr_test.bin", "w")


def convert_to_binary(number):
    binary_str = bin(number)[2:]
    binary_32_bit = binary_str.zfill(32)
    return binary_32_bit
 

instr_memory = [
    0b00000000101000000000000010010011,
    0b11111111110100001000000100010011,
    0b00000000001000001000000110110011,
    1081491
]

class Transaction (Instruction):
    def __init__(self) -> None:
        super().__init__()

class RandomALUTest:
    def __init__(self) -> None:
        #self.test_set = [InstructionADD, InstructionADDI, InstructionSUB, InstructionXOR, InstructionXORI, InstructionOR, InstructionORI, InstructionAND, InstructionANDI, InstructionSLT, InstructionSLTI, InstructionSLTU, InstructionSLTIU, InstructionSLL, InstructionSLLI, InstructionSRL, InstructionSRLI, InstructionSRAI, InstructionSRA]
        self.test_set = [InstructionADD, InstructionADDI, InstructionSUB, InstructionXOR, InstructionXORI, InstructionOR, InstructionORI, InstructionAND, InstructionANDI, InstructionSLT, InstructionSLTI, InstructionSLTU, InstructionSLTIU, InstructionSLL, InstructionSLLI, InstructionSRL, InstructionSRLI, InstructionSRA]
        #self.test_set = [InstructionADD, InstructionADDI, InstructionSUB, InstructionXOR, InstructionXORI, InstructionOR, InstructionORI, InstructionAND, InstructionANDI, InstructionSLT, InstructionSLTI, InstructionSLTU, InstructionSLTIU]

    def get_inst(self, variant):
        instr_cls = random.choice(self.test_set)
        instr_inst = instr_cls()
        instr_inst.randomize(variant)
        return instr_inst

class Program:
    def __init__(self, instrs) -> None:
        self.instrs = instrs
        self.current_idx = -1

    def get_inst(self, variant):
        self.current_idx += 1
        if self.current_idx > (len(self.instrs) -1 ):
            self.current_idx -= 1

        return self.instrs[self.current_idx]



class FIFO:
    def __init__(self) -> None:
        self.queue = []
        self.pushed = Event()
        self.poped = Event()
        pass

    async def push (self, pkt):
        if len(self.queue) >= 1:
            cocotb.log.info("Awaiting packet read")
            await self.poped.wait()
        self.queue.append(pkt)
        self.poped.clear()
        self.pushed.set()

        return 1

    async def pop (self):
        if len(self.queue) == 0:
            cocotb.log.info("Awaiting port write")
            await self.pushed.wait()
        return self.queue.pop()

    def done(self):
        self.poped.set()
        self.pushed.clear()
        return 1


    def peek (self):
        return self.queue[0]

class Driver:
    def __init__(self, dut, gen_port : FIFO) -> None:
        self.fifo_gen_port = gen_port
        self.dut = dut
        pass

    async def reset_dut(self):
        # Reset sequence
        self.dut.rst_n.value = 1
        await Timer(0.5, units="ns")
        self.dut.rst_n.value = 0
        await Timer(1, units="ns")
        self.dut.rst_n.value = 1

        return 1

    async def drive_dut(self, tx_pkt : Transaction):
        cocotb.log.info(f"Driving dut ports with packet {str(tx_pkt)}")
        self.dut.instr.value = tx_pkt.encode()
        await RisingEdge(self.dut.clk)
        await FallingEdge(self.dut.clk)
        return 1
    
    async def main(self):
        await self.reset_dut()
        cocotb.log.info("Reset Done")
        while True:
            tx = await self.fifo_gen_port.pop()
            await self.drive_dut(tx)
            self.fifo_gen_port.done()

class Generator:
    def __init__(self, gen_port : FIFO, test) -> None:
        self.fifo_port = gen_port
        self.test = test
    
    async def main(self):
        while True:
            pkt = self.test.get_inst(RV32I)
            out_instr.write(convert_to_binary(pkt.encode()) + "\n")
            await self.fifo_port.push(pkt)
        #for pkt in test.insns:
        #    await self.fifo_port.push(pkt)
        return 1

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
#coverage definition  
INST_Coverage = coverage_section (
  CoverPoint("top.instr", xf=lambda  instr : instr&0x7F, bins=[0b0110011, 0b0010011, 0b0000011, 0b1110011], bins_labels=["Arith", "Arith imm", "Load Store", "Illegal"]),
)

class Monitor:
    def __init__(self, dut) -> None:
        self.dut = dut
        self.ref_model = Model(RV32I)


    # calling coverage / sampling coverage 
    @INST_Coverage   
    def sample(self, instr):
        print(instr)
        pass

    async def main(self):
        while True:
            await RisingEdge(self.dut.clk)
            if not self.dut.instr.value.is_resolvable:
                continue

            print("DEBUG AKARSH", type(self.dut.instr.value), self.dut.instr.value)
            instr = decode(self.dut.instr.value)
            alu_out = self.dut.alu_inst.out.value
            self.ref_model.execute(instr)

            # Register updates at falling edge
            await FallingEdge(self.dut.clk)
            await Timer(0.1, units="ns")
            regs = [i.value for i in self.dut.register_file_inst.reg_mem.value]
            expected_reg = [i.unsigned() for i in self.ref_model.state.intreg.regs]
            expected_reg.reverse()
            cocotb.log.info(f"Instruction {instr}")
            self.sample(instr.encode())
            #continue
            if (regs == expected_reg):
                cocotb.log.info(f"Correctly executed {instr}")
            else:
                cocotb.log.info(f"Mismatch {instr}")
                cocotb.log.info(f"Executed value = {regs}" )
                cocotb.log.info(f"Expected value = {expected_reg}")
                cocotb.log.info(f"ALU output = {alu_out.value}")
                self.mismatch += 1
                out_instr.close()
                assert 0
            
            
        return 1



## Test ALU instructions
@cocotb.test()
async def random_alu(dut):
    print("Running random ALU")
    """Try accessing the design."""

    clock = Clock(dut.clk, 2, units="ns")
    dut.stall.value = 0
    cocotb.start_soon(clock.start(start_high=False))

    dri_gen_port = FIFO()
    dri = Driver(dut, dri_gen_port)
    random_alu_test = RandomALUTest()
    gen = Generator(dri_gen_port, random_alu_test)
    mon = Monitor(dut)
    cocotb.start_soon(gen.main())
    cocotb.start_soon(dri.main())
    cocotb.start_soon(mon.main())

    await Timer(1000, units="ns")  # wait a bit
    out_instr.close()
    #assert mon.mismatch == 0
    print("Final state")
    print([i.value for i in dut.register_file_inst.reg_mem.value])
    coverage_db.report_coverage(cocotb.log.info, bins=True)
    coverage_db.export_to_xml(filename="coverage_fifo.xml")
    coverage_db.export_to_yaml(filename="coverage_fifo.yml")



## TEST load and store instructions 
# 1. Make initial reg and memory state
# 2. Create memory software model
# 2. Create random load and store instruction streams
# 3.
#@cocotb.test()
async def directed_load_store(dut):

    clock = Clock(dut.clk, 2, units="ns")
    dut.stall.value = 0
    cocotb.start_soon(clock.start(start_high=False))

    dri_gen_port = FIFO()
    dri = Driver(dut, dri_gen_port)
    prog = Program([
                InstructionADDI(x1, x0, 0xde),
                InstructionSLLI(x1, x1, 8),
                InstructionADDI(x1, x1, 0xad),
                InstructionSLLI(x1, x1, 8),
                InstructionADDI(x1, x1, 0xbe),
                InstructionSLLI(x1, x1, 8),
                InstructionADDI(x1, x1, 0xef),
                InstructionLB(x2, x0, 0),
                InstructionLH(x3, x0, 0),
                InstructionLW(x4, x0, 0),
                InstructionSB(x0, x1, 4),
                InstructionSB(x0, x1, 5),
                InstructionSH(x0, x1, 8),
                InstructionSH(x0, x1, 10),
                InstructionSW(x0, x1, 12),
            ])
    mem = MemoryModel(dut)
    mem.mem[0] = 0xdeadbeef
    gen = Generator(dri_gen_port, prog)
    mon = Monitor(dut)
    cocotb.start_soon(gen.main())
    cocotb.start_soon(dri.main())
    cocotb.start_soon(mon.main())
    cocotb.start_soon(mem.run_mem())

    await Timer(32, units="ns")  # wait a bit
    out_instr.close()
    # changes by akarsh 
    #assert mon.mismatch == 0
    print("Final state")
    print([i.value for i in dut.register_file_inst.reg_mem.value])
    print(mem.mem)
    print(list(map(hex, mem.mem.values())))
    coverage_db.report_coverage(cocotb.log.info, bins=True)
    coverage_db.export_to_xml(filename="coverage_fifo.xml")
    coverage_db.export_to_yaml(filename="coverage_fifo.yml")


    
# How to do functional coverage ?
# There is a mismatch in Driving dut port and instruction -> Cycle delay, checking after next packet
    
# Write a generator for directed execution as well -> assembly hex file
# Write instructions to output
