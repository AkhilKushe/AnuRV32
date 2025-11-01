from pyuvm import *
import random
from riscvmodel.insn import *
from riscvmodel.variant import RV32I

class AnuSeqItem (uvm_sequence_item):
    test_set = [InstructionADD, InstructionADDI, InstructionSUB, InstructionXOR, InstructionXORI, InstructionOR, InstructionORI, InstructionAND, InstructionANDI, InstructionSLT, InstructionSLTI, InstructionSLTU, InstructionSLTIU, InstructionSLL, InstructionSLLI, InstructionSRL, InstructionSRLI, InstructionSRA]
    def __init__(self, name):
        super().__init__(name)
        self.stall = 0
        self.instr = 0
        self.data_in = 0
        self.pc_o = 0
        self.data_out= 0
        self.mem_addr = 0
        self.mem_access_mode = 0

        ## Other members 
        self.instr_type = None
        self.reg_mem = []

    def randomize(self):
        self.instr_type = random.choice(AnuSeqItem("tr").test_set)
        self.instr = self.instr_type() 
        self.instr.randomize(RV32I)

    def __str__(self):
        buff = ""
        for attr in vars(self).keys():
            buff += f" {attr} : {getattr(self, attr)} "
        
        return buff