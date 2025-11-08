from pyuvm import *
import random

class MemSeqItemBase (uvm_sequence_item):
    def __init__(self, name):
        super().__init__(name)
        #self.seq_type = ConfigDB().get(None, ".", "MEM_SEQ_TYPE", None)
        #if self.test_set is None:
        #    uvm_fatal(self.get_type_name(), " : Mem sequence type not found")

        self.data_in = 0
        self.data_out= 0
        self.mem_addr = 0
        self.mem_access_mode = 0

    # Randomize type
    def randomize(self):
        pass

    def __str__(self):
        buff = ""
        for attr in vars(self).keys():
            buff += f" {attr} : {getattr(self, attr)} "
        return buff