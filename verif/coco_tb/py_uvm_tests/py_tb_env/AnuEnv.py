from pyuvm import *
import AnuDriver as AnuDriver
import AnuMonitor
import AnuScoreboard

class AnuEnv (uvm_env):
    def build_phase(self):
        self.seqr = uvm_sequencer("seqr", self)
        ConfigDB().set(None, "*", "SEQR", self.seqr)
        self.driver = AnuDriver.AnuDriver.create("driver", self)
        self.apb_mon = AnuMonitor.AnuMonitor("apb_mon", self, "sample")
        self.scoreboard = AnuScoreboard.AnuScoreboard("scoreboard", self)

    def connect_phase(self):
        self.driver.seq_item_port.connect(self.seqr.seq_item_export)
        self.apb_mon.ap.connect(self.scoreboard.result_export)