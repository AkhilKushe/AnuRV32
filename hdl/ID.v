// Decode the instructions and output all the control signals, this should be the control bus ?
// Control unit will orchestrate


module instr_decode (instr, rst_n, rs1, rs2, rd, alu_uop, opcode, imm, f7, ctrlSig);
input [31:0]instr;
input rst_n;
output [4:0] rs1;
output [4:0] rs2;
output [4:0] rd;
output [2:0] alu_uop;
output [6:0] opcode;
output [31:0] imm;
output f7;

output [15:0] ctrlSig;

assign f7 = instr[30];
assign rs2 = instr[24:20];
assign rs1 = instr[19:15];
assign rd = instr[11:7];
assign alu_uop = instr[14:12];
assign opcode = instr[6:0];


uCode_decode uCode (.alu_uop(alu_uop),
			.opcode(opcode),
			.ctrlSig(ctrlSig));

extract_imm extract_imm_inst (.ctrlSig(ctrlSig),
			.instr(instr),
			.imm(imm),
			.rst_n(rst_n));

endmodule

/*
MSB ---------------- LSB
X, X, X, X, X, X, LUI, AUIPC, JAL, JALR, Branch, STORE, LOAD, Shift-OP, I-Frame, ALU_op
*/

import "DPI-C" function string getenv(input string env_name); 
module uCode_decode (alu_uop, opcode, ctrlSig);
input [6:0] opcode;
input [2:0] alu_uop;
output [15:0] ctrlSig;
reg [15:0] ctrlSig_t;
reg [15:0] uCode [127:0];
wire shift_op;

initial begin 
	$readmemb(getenv("UCODE"), uCode);
end

always @(*) begin
	ctrlSig_t = uCode[opcode];
end

assign shift_op = ctrlSig_t[0] & (alu_uop == 3'b101 | alu_uop == 3'b001);
assign ctrlSig = (ctrlSig_t | {13'b0000000000000, shift_op,2'b00});

endmodule

// Return sign extended immediate instruction
// TODO, not extracting imm correctly for LOAD/STORE
module extract_imm (ctrlSig, instr, imm, rst_n);
input [15:0]ctrlSig;
input [31:0] instr;
input rst_n;
output reg [31:0] imm;

always @(*) begin
	if (~rst_n) begin
		imm = 32'd0;
	end else begin
		if (ctrlSig[1]) begin // I type
			imm = {{21{instr[31]}}, instr[30:20]}; // If its is I frame, sign extend for immediate
			imm = ctrlSig[2] ? {27'd0, instr[24:20]} : imm; //If shift operation, take unsigned shift amount
		end else if (ctrlSig[4]) begin	//S type
			imm = {{21{instr[31]}}, instr[30:25], instr[11:7]};
		end else if (ctrlSig[5]) begin // B type
			imm = {{20{instr[31]}},instr[7], instr[30:25],instr[11:8],1'b0};
		end else if (ctrlSig[8] | ctrlSig[9]) begin // U type
			imm = {instr[31:12], {12{1'b0}}};
		end else if (ctrlSig[7]) begin // J type
			imm = {{11{instr[31]}}, instr[19:12], instr[20], instr[30:21],1'b0};
		end else begin
			imm = 32'd0;
		end
	end
end

endmodule
