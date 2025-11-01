import cocotb_bus.bus
from pyuvm import *
import cocotb_bus
from cocotb.triggers import RisingEdge

class AnuDriver (uvm_driver):
    def build_phase (self):
        self.anu_core_bus = ConfigDB().get(self, ".", "BFM", None)
        if self.anu_core_bus is None:
            uvm_error(self.get_type_name(), " : NO_BFM_FOUND")

    async def run_phase(self):
        await self.anu_core_bus.dut_reset()
        self.logger.info("Done Reset")
        while True:
            cmd = await self.seq_item_port.get_next_item()
            pc = await self.anu_core_bus.execute_instr(cmd)
            self.seq_item_port.item_done()