from cocotb_bus.bus import Bus
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from riscvmodel.code import decode
from MemSequenceItemBase import MemSeqItemBase

def get_val (signal):
    if signal.is_resolvable:
        return int(signal)
    else:
        return 0 

class MemIntfBase () :
    def __init__(self, entity, sysclk):
        self.dut = entity
        self.sysclk = sysclk
        self.mem_access_mode = self.dut.mem_access_mode
        self.data_in = self.dut.data_out
        self.data_out = self.dut.data_in
        self.addr= self.dut.mem_addr
    
    async def write(self, tx : MemSeqItemBase):
        self.dut.data_in.value = tx.data_in 
        await RisingEdge(self.sysclk)


    def sample(self, seq : MemSeqItemBase):
        seq.data_in = get_val(self.dut.data_in.value)
        seq.data_out = get_val(self.dut.data_out.value)
        seq.mem_addr = get_val(self.dut.mem_addr.value)
        seq.mem_access_mode = get_val(self.dut.mem_access_mode.value)
        return seq