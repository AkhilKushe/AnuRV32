import sys
from pathlib import Path
sys.path.append(str(Path("py_tb_env").resolve()))
sys.path.insert(0, (str(Path("../../RVmodel/riscv-python-model/").resolve())))

import cocotb
from cocotb.clock import Clock
import pyuvm
from pyuvm import *
from py_tb_env import AnuEnv, AnuCoreBus, AnuDriver, AnuMonitor, AnuScoreboard, AnuSeqItem, AnuSequence
from riscvmodel.insn import *

@pyuvm.test()
class random_alu_wo_SRAI (uvm_test):
    def build_phase(self):
        print("base_test build phase")
        self.clock = Clock(cocotb.top.clk, 1, units="ns")
        ConfigDB().set(None, "*", "BFM", AnuCoreBus.AnuCoreBus(cocotb.top, self.clock.signal))
        ConfigDB().set(None, "*", "TEST_SET", [InstructionADD, InstructionADDI, InstructionSUB, InstructionXOR, InstructionXORI, InstructionOR, InstructionORI, InstructionAND, InstructionANDI, InstructionSLT, InstructionSLTI, InstructionSLTU, InstructionSLTIU, InstructionSLL, InstructionSLLI, InstructionSRL, InstructionSRLI, InstructionSRA])
        self.env = AnuEnv.AnuEnv("env", self)

    def end_of_elaboration_phase(self):
        print("Base test end of elab stage")
        self.test_all = AnuSequence.AnuSeq.create("test_all")

    async def run_phase(self):
        print("Base test run_phase")
        cocotb.start_soon(self.clock.start(start_high=False))
        self.raise_objection()
        await self.test_all.start()
        self.drop_objection()
        print("DONEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEee")
        print("Final state")
        print([i.value for i in cocotb.top.register_file_inst.reg_mem.value])

    

#@pyuvm.test()
class random_alu_all (uvm_test):
    def build_phase(self):
        print("base_test build phase")
        self.clock = Clock(cocotb.top.clk, 1, units="ns")
        ConfigDB().set(None, "*", "BFM", AnuCoreBus.AnuCoreBus(cocotb.top, self.clock.signal))
        ConfigDB().set(None, "*", "TEST_SET", [InstructionADD, InstructionADDI, InstructionSUB, InstructionXOR, InstructionXORI, InstructionOR, InstructionORI, InstructionAND, InstructionANDI, InstructionSLT, InstructionSLTI, InstructionSLTU, InstructionSLTIU, InstructionSLL, InstructionSLLI, InstructionSRL, InstructionSRLI, InstructionSRA, InstructionSRAI])
        self.env = AnuEnv.AnuEnv("env", self)

    def end_of_elaboration_phase(self):
        print("Base test end of elab stage")
        self.test_all = AnuSequence.AnuSeq.create("test_all")

    async def run_phase(self):
        print("Base test run_phase")
        cocotb.start_soon(self.clock.start(start_high=False))
        self.raise_objection()
        await self.test_all.start()
        self.drop_objection()
        print("DONEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEee")
        print("Final state")
        print([i.value for i in cocotb.top.register_file_inst.reg_mem.value])

    
