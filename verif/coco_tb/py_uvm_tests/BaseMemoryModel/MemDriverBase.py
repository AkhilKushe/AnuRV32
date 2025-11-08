import cocotb_bus.bus
from pyuvm import *
import cocotb_bus
from cocotb.triggers import RisingEdge, First, Edge

class MemDriverBase (uvm_driver):
    def build_phase (self):
        self.mem_bus_if = ConfigDB().get(self, ".", "mem_bus_if", None)
        if self.mem_bus_if is None:
            uvm_error(self.get_type_name(), " : mem_bus_if not found")

        self.initiate_memory = ConfigDB().get(self, ".", "INITIAL_MEM", None)
        if self.initiate_memory is None:
            self.logger.info("No initial memory state")
            self.mem = {}
        else:
            self.logger.info("Memory initialized with user state")
            self.mem = self.initiate_memory
    
    def reset(self):
        self.mem = {}

    async def run_phase(self):
        while True:
            await First(Edge(self.mem_bus_if.addr), Edge(self.mem_bus_if.data_in), Edge(self.mem_bus_if.mem_access_mode))
            #if self.addr.value % 4 != 0:
            #    self.dut.log("Unaligned memory access will be ignored at %d"%(self.addr.value))
            if not (self.mem_bus_if.mem_access_mode.value.is_resolvable and self.mem_bus_if.addr.value.is_resolvable and self.mem_bus_if.data_in.value.is_resolvable):
                continue

            self.logger.info(self.mem_bus_if.mem_access_mode.value)
            if(self.mem_bus_if.mem_access_mode == 0) :
                ## Read mode
                self.mem_bus_if.data_out.value = self.get_addr(self.mem_bus_if.addr.value.integer)

            elif self.mem_bus_if.mem_access_mode == 1:
                ## Write byte
                self.set_b(self.mem_bus_if.addr.value.integer, self.mem_bus_if.data_in.value.integer)

            elif self.mem_bus_if.mem_access_mode == 2:
                ## Write Half word
                self.set_hw(self.mem_bus_if.addr.value.integer, self.mem_bus_if.data_in.value.integer)

            elif self.mem_bus_if.mem_access_mode == 3:
                ## Write Full word
                self.set_w(self.mem_bus_if.addr.value.integer, self.mem_bus_if.data_in.value.integer)

            else:
                self.logger.error("Illegal memory access value")


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

    def report_phase(self):
        self.logger.info(f"Memory state at the end :")
        for k, v in self.mem.items():
            print(f"{k}, {hex(v)}")
        return super().report_phase()
    