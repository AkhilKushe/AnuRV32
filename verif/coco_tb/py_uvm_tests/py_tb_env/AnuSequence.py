from pyuvm import *
import AnuSeqItem as AnuSeqItem

NUM_INSTRS = 100
class AnuSeq(uvm_sequence):
    async def body(self):
        seqr = ConfigDB().get(None, "", "SEQR")
        random = RandomSeq.create("random")
        cocotb.log.info("in Anu seq body")
        await random.start(seqr)

class RandomSeq(uvm_sequence):
    async def body(self):
        for _ in range(NUM_INSTRS):
            tr = AnuSeqItem.AnuSeqItem("tr")
            await self.start_item(tr)
            tr.randomize()
            cocotb.log.info(f"Transaction {tr}")
            await self.finish_item(tr)

class DirectedSeq(uvm_sequence):
    async def body(self):
        directed_test = ConfigDB().get(None, "", "DIRECTED_TEST", [])
        for t in directed_test:
            tr = AnuSeqItem.AnuSeqItem("tr")
            await self.start_item(tr)
            tr.instr_type = type(t)
            tr.instr = t
            cocotb.log.info(f"Transaction {tr}")
            await self.finish_item(tr) 