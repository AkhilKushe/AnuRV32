from cocotb_bus.bus import Bus
from cocotb.triggers import RisingEdge, FallingEdge, Timer
from AnuSeqItem import AnuSeqItem
from riscvmodel.code import decode

def get_val (signal):
    if signal.is_resolvable:
        return int(signal)
    else:
        return 0 

class AnuCoreBus () :
    def __init__(self, entity, sysclk):
        self.dut = entity
        self.sysclk = sysclk
    
    async def execute_instr(self, tx : AnuSeqItem):
        self.dut.stall.value = tx.stall 
        self.dut.instr.value = tx.instr.encode()
        self.dut.data_in = 0
        await RisingEdge(self.sysclk)
        return get_val(self.dut.pc_o.value)

    async def dut_reset (self):
        # Reset sequence
        self.dut.rst_n.value = 1
        await Timer(0.5, units="ns")
        self.dut.rst_n.value = 0
        await Timer(1, units="ns")
        self.dut.rst_n.value = 1
        await RisingEdge(self.sysclk)


    def sample(self, seq : AnuSeqItem):
        seq.stall = get_val(self.dut.stall.value)
        seq.instr = get_val(self.dut.instr.value)
        if seq.instr == 0:
            seq.instr = None
        else:
            seq.instr = decode(seq.instr)
        seq.data_in = get_val(self.dut.data_in.value)
        seq.pc_o = get_val(self.dut.pc_o.value)
        seq.data_out= get_val(self.dut.data_out.value)
        seq.mem_addr = get_val(self.dut.mem_addr.value)
        seq.mem_access_mode = get_val(self.dut.mem_access_mode.value)
        seq.instr_type = None
        seq.reg_mem = [get_val(i) for i in self.dut.register_file_inst.reg_mem.value]
        return seq
