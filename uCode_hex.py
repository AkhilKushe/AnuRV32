

fileName = "uCode.hex"

fp = open(fileName, "w")

alu_op = 1 
i_frame = 1 << 1
shift_op = 1 << 2
load = 1 << 3
store = 1 << 4
branch = 1 << 5
jalr = 1 << 6
jal = 1 << 7
auipc = 1 << 8
lui = 1 << 9
nop = 0

opCodes = {
            0b0110111 : lui ,
            0b0010111 : auipc,
            0b1101111 : jal,
            0b1100111 : jalr | i_frame,
            0b1100011 : branch,
            0b0000011 : load | i_frame,
            0b0100011 : store,
            0b0010011 : alu_op | i_frame,
            0b0110011 : alu_op,
            0b0001111 : nop, #Fence/Pause
            0b1110011 : nop,
        }
mem = []

for addr in range(128):
    fp.write("{:016b}".format(opCodes.get(addr, nop)) + "\n")

fp.close()



