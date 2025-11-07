import cocotb.result
from riscvmodel.model import Model
from riscvmodel.variant import RV32I
from riscvmodel.code import decode
from pyuvm import *

class AnuScoreboard(uvm_component):
    def __init__(self, name, parent):
        super().__init__(name, parent)
        self.ref_model = Model(RV32I)

    def build_phase(self):
        self.result_fifo = uvm_tlm_analysis_fifo("result_fifo", self)
        self.result_get_port = uvm_get_port("result_get_port", self)
        self.result_export = self.result_fifo.analysis_export

    def connect_phase(self):
        self.result_get_port.connect(self.result_fifo.get_export)

    def check_phase(self):
        while self.result_get_port.can_get():
            _, time_result = self.result_get_port.try_get()
            actual_result, t = time_result
            self.logger.info(f"GOT {actual_result}") 

            if not actual_result.instr:
                continue

            instr = actual_result.instr
            self.ref_model.execute(instr)
            regs = actual_result.reg_mem
            expected_reg = [i.unsigned() for i in self.ref_model.state.intreg.regs]
            expected_reg.reverse()

            if (regs == expected_reg):
                self.logger.info(f"Correctly executed {instr} @ {t}")
            else:
                self.logger.info(f"Mismatch {instr}, {instr.encode()} @ {t}")
                self.logger.info(f"Executed value = {regs}" )
                self.logger.info(f"Expected value = {expected_reg}")
                raise cocotb.result.TestError()