import sys
from pathlib import Path
sys.path.append(str(Path("py_tb_env").resolve()))
sys.path.append(str(Path("BaseMemoryModel").resolve()))
sys.path.insert(0, (str(Path("../../RVmodel/riscv-python-model/").resolve())))

import cocotb
from cocotb.clock import Clock
import pyuvm
from pyuvm import *
from py_tb_env import AnuEnv, AnuCoreBus, AnuDriver, AnuMonitor, AnuScoreboard, AnuSeqItem, AnuSequence
from BaseMemoryModel.MemInterfaceBase import MemIntfBase
from riscvmodel.insn import *
from riscvmodel.regnames import *

#@pyuvm.test()
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

@pyuvm.test()
class random_mem_load_store (uvm_test):
    def build_phase(self):
        print("base_test build phase")
        self.clock = Clock(cocotb.top.clk, 1, units="ns")
        ConfigDB().set(None, "*", "BFM", AnuCoreBus.AnuCoreBus(cocotb.top, self.clock.signal))
        ConfigDB().set(None, "*", "mem_bus_if", MemIntfBase(cocotb.top, self.clock.signal))
        ConfigDB().set(None, "*", "TEST_SET", [])
        ConfigDB().set(None, "*", "DIRECTED_TEST", [
            InstructionADDI(x1, x0, 0xde),
            InstructionSLLI(x1, x1, 8),
            InstructionADDI(x1, x1, 0xad),
            InstructionSLLI(x1, x1, 8),
            InstructionADDI(x1, x1, 0xbe),
            InstructionSLLI(x1, x1, 8),
            InstructionADDI(x1, x1, 0xef),
            InstructionLBU(x2, x0, 0),
            InstructionLHU(x3, x0, 0),
            InstructionLW(x4, x0, 0),
            InstructionSB(x0, x1, 4),
            InstructionSB(x0, x1, 5),
            InstructionSH(x0, x1, 8),
            InstructionSH(x0, x1, 10),
            InstructionSW(x0, x1, 12),
        ])
        ConfigDB().set(None, "*", "INITIAL_MEM", {3: 0xde, 2:0xad, 1:0xbe, 0:0xef})
        self.env = AnuEnv.AnuEnv("env", self)
        uvm_factory().set_type_override_by_type(AnuSequence.RandomSeq, AnuSequence.DirectedSeq)

    def end_of_elaboration_phase(self):
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
