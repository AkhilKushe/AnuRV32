import cocotb.utils
from pyuvm import *
from cocotb.triggers import RisingEdge
from MemSequenceItemBase import MemSeqItemBase

class MemMonitorBase (uvm_component):
    def __init__(self, name, parent, method_name):
        super().__init__(name, parent)
        self.method_name = method_name
        self.ap = uvm_analysis_port("ap", self)

    def build_phase(self):
        self.mem_bus_if = ConfigDB().get(self, ".", "mem_bus_if", None)
        if self.mem_bus_if is None:
            uvm_error(self.get_type_name(), " : mem_bus_if not found")
        self.get_method = getattr(self.mem_bus_if, self.method_name)

    async def run_phase(self):
        while True:
            await RisingEdge(self.mem_bus_if.sysclk)
            rx = MemSeqItemBase("rx")
            datum = self.get_method(rx)
            self.logger.info(f"MONITORED {datum}")
            self.ap.write((datum, cocotb.utils.get_sim_time(units="ns")))
