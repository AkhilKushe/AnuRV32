import sys
from pathlib import Path

import cocotb.simulator
sys.path.append(str(Path("py_tb_env").resolve()))

import cocotb
from cocotb.triggers import FallingEdge, Timer, RisingEdge, Edge, Event
from cocotb.clock import Clock
import random
import pyuvm
from pyuvm import *
from py_tb_env import AnuEnv, AnuCoreBus, AnuDriver, AnuMonitor, AnuScoreboard, AnuSeqItem, AnuSequence

@pyuvm.test()
class random_alu (uvm_test):
    def build_phase(self):
        print("base_test build phase")
        self.clock = Clock(cocotb.top.clk, 1, units="ns")
        ConfigDB().set(None, "*", "BFM", AnuCoreBus.AnuCoreBus(cocotb.top, self.clock.signal))
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

    
