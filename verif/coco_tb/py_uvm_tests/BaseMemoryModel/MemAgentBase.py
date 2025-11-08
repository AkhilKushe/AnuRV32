from pyuvm import *
from MemDriverBase import MemDriverBase
from MemMonitorBase import MemMonitorBase

class MemAgentBase (uvm_agent):
    def build_phase(self):
        self.mem_driver = MemDriverBase.create("mem_driver", self)
        self.mem_mon = MemMonitorBase("mem_mon", self, "sample")
        self.ap_port = self.mem_mon.ap

#    def connect_phase(self):
        #self.mem_mon.ap.connect(self.ap_port.get_expo)