from pyuvm import *
import AnuDriver as AnuDriver
import AnuMonitor
import AnuScoreboard
from MemAgentBase import MemAgentBase

class AnuEnv (uvm_env):
    def build_phase(self):
        self.seqr = uvm_sequencer("seqr", self)
        ConfigDB().set(None, "*", "SEQR", self.seqr)
        self.driver = AnuDriver.AnuDriver.create("driver", self)
        self.anu_mon = AnuMonitor.AnuMonitor("apb_mon", self, "sample")
        self.scoreboard = AnuScoreboard.AnuScoreboard("scoreboard", self)
        self.mem_agent = MemAgentBase.create("agent", self)

    def connect_phase(self):
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)
        self.anu_mon.ap.connect(self.scoreboard.result_export)
        self.mem_agent.ap_port.connect(self.scoreboard.mem_export)