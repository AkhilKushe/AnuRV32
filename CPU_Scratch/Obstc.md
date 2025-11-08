1. Similatior crash
- SImulator crashed due to race condition
- Crash in cocotb, design loaded again in modelsim
- Crash most likely due to registerfile implementation

-> Creating combo loop while register writeback, not design mistake but typo
assign rd_data_w = (jal | jalr)  ? pc_w + 4 : data_wb_w; -> wrong
assign rd_data_w = (jal | jalr)  ? pc_w + 4 : data_wb_r; -> correct

I was assigning write instead of the registered output

2. Fixing bugs
i. Caught bug in logical ops
- wong op code assigned for xor and and operation

ii. Fix in model
- instruction execute function was taking state instead of model

ii. Bug in sltiu
- Appears to be an issue with model again
- Model doing signed comparions instead of unsinged

iii. Bug with shift operations (R2R)
- shift amount is lower 5 bits of rs2

iv. SRA, SRAI
- SRA, srai, bug in design, not doing signed arithmatic shift
- bug in model, not doing signed arithmatic shift for SRAI, srai was passing
- MOdel bug fixed
- Design bug, added $signed still not fixed, why ??
- interesting bug, needed to make signed wire, not happening with $signed in mux select line

---------------------------- ALU looks good -------------------------------------------------

Memory load store equation :
i. Found bug in load instruction
    - lb, lh are signed loading
    - lbu, lhu are unsigned loads
    Current I think I have only implemented lb or lh in unsigned mode
