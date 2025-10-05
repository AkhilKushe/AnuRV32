from cocotb.triggers import Edge, First
from cocotb.binary import BinaryValue

#Byte addressible memory
class MemoryModel:
    def __init__(self, dut) -> None:
        self.reset()
        self.attact_memory(dut)

    def attact_memory(self, dut):
        self.dut = dut
        self.addr = dut.mem_addr
        self.data_out = dut.data_in
        self.data_in = dut.data_out
        self.mem_access_mode = dut.mem_access_mode
    
    def reset(self):
        self.mem = {}

    async def run_mem(self):
        # Restrict to 20 read writes
        for i in range(50):
            sig  = await First(Edge(self.addr), Edge(self.data_in), Edge(self.mem_access_mode))
            #if self.addr.value % 4 != 0:
            #    self.dut.log("Unaligned memory access will be ignored at %d"%(self.addr.value))
            if not (self.mem_access_mode.value.is_resolvable and self.addr.value.is_resolvable and self.data_in.value.is_resolvable):
                continue

            self.dut.log.info(self.mem_access_mode.value)
            self.dut.log.info(i)
            if(self.mem_access_mode.value == 0) :
                ## Read mode
                self.data_out.value = self.get_addr(self.addr.value.integer)

            elif self.mem_access_mode.value == 1:
                ## Write byte
                self.set_b(self.addr.value.integer, self.data_in.value.integer)

            elif self.mem_access_mode.value == 2:
                ## Write Half word
                self.set_hw(self.addr.value.integer, self.data_in.value.integer)

            elif self.mem_access_mode.value == 3:
                ## Write Full word
                self.set_w(self.addr.value.integer, self.data_in.value.integer)

            else:
                self.dut.log("Illegal memory access value")


    def set_b(self, addr, data):
        self.mem[addr] = data & 0xff
    
    def set_hw(self, addr, data):
        self.mem[addr] = data & 0xff
        self.mem[addr+1] = (data >> 8) & 0xff

    def set_w(self, addr, data):
        self.mem[addr] = data & 0xff
        self.mem[addr+1] = (data >> 8) & 0xff
        self.mem[addr+2] = (data >> 16) & 0xff
        self.mem[addr+3] = (data >> 24) & 0xff

    
    def get_addr(self, addr):
        # Little endian memory access
        data = (self.mem.get(addr+3, 0)<<8*3) | (self.mem.get(addr+2, 0)<<8*2) | (self.mem.get(addr+1, 0)<<8) | self.mem.get(addr, 0)
        return data

    





