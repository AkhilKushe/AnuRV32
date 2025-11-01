import cocotb.utils
from pyuvm import *
from cocotb.triggers import RisingEdge
import AnuSeqItem as AnuSeqItem

class AnuMonitor (uvm_component):
    def __init__(self, name, parent, method_name):
        super().__init__(name, parent)
        self.method_name = method_name

    def build_phase(self):
        self.ap = uvm_analysis_port("ap", self)
        self.anu_core_bus = ConfigDB().get(self, ".", "BFM", None)
        if self.anu_core_bus is None:
            uvm_error(self.get_type_name(), " : NO_BFM_FOUND")
        self.get_method = getattr(self.anu_core_bus, self.method_name)

    async def run_phase(self):
        while True:
            await RisingEdge(self.anu_core_bus.sysclk)
            rx = AnuSeqItem.AnuSeqItem("rx")
            datum = self.get_method(rx)
            self.logger.info(f"MONITORED {datum}")
            self.ap.write((datum, cocotb.utils.get_sim_time(units="ns")))
