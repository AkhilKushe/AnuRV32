from pyuvm import *
import random
from riscvmodel.insn import *
from riscvmodel.variant import RV32I

class AnuSeqItem (uvm_sequence_item):
    def __init__(self, name):
        super().__init__(name)
        self.test_set = ConfigDB().get(None, ".", "TEST_SET", None)
        if self.test_set is None:
            uvm_fatal(self.get_type_name(), " : TEST_SET not foudn")

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
        self.instr_type = random.choice(self.test_set)
        self.instr = self.instr_type() 
        self.instr.randomize(RV32I)

    def __str__(self):
        buff = ""
        for attr in vars(self).keys():
            if attr == "test_set":
                continue
            buff += f" {attr} : {getattr(self, attr)} "
        
        return buff