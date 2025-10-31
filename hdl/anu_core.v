module anu_core (stall, instr, data_in, rst_n, clk, pc_o, data_out, mem_addr, mem_access_mode);

input stall;
input [31:0] instr;
input [31:0] data_in;
input rst_n;
input clk;

output [31:0] pc_o;
output [31:0] data_out;
output [31:0] mem_addr;
output reg [1:0] mem_access_mode;

wire [4:0] rs1_w;
wire [4:0] rs2_w;
wire [4:0] rd_w;
reg [4:0] rd_r;

wire [31:0] imm_w;
wire [31:0] op1_w;
wire [31:0] op1_pc_w;
wire [31:0] op2_imm_w;
wire [31:0] op2_w;

wire [2:0] uop_w;
reg [2:0] alu_uop_r;
wire f7_w;
reg valid_f7_r;
wire wen_w;
reg wen_r;
reg branch_r;
wire zero_w;

wire [15:0] ctrlSig_w;
wire [31:0] extended_data_in;
wire [31:0] alu_out_w;
wire [31:0] alu_out_imm_w;
wire [31:0] data_wb_w;
reg [31:0] data_wb_r;
wire [31:0] rd_data_w;

reg [1:0] mem_access_mode_r;
wire b_hbar_w, bypass_w, sig_w;

// PC wires
wire pc_mode0_w;
wire pc_mode1_w;
wire [31:0] pc_imm_w;
wire [1:0] pc_mode_w;
wire [31:0] pc_w;

wire alu_op, i_frame, shift_op, ld, st, branch_op, jalr, jal, auipc, lui;
wire sign_w;

//Alias, fix in ctrl unit
assign alu_op = ctrlSig_w[0];
assign i_frame = ctrlSig_w[1];
assign shift_op = ctrlSig_w[2];
assign ld = ctrlSig_w[3];
assign st = ctrlSig_w[4];
assign branch_op = ctrlSig_w[5];
assign jalr = ctrlSig_w[6];
assign jal = ctrlSig_w[7];
assign auipc = ctrlSig_w[8];
assign lui = ctrlSig_w[9];





instr_decode instr_decode_inst(.instr(instr), 
				.rst_n(rst_n), 
				.rs1(rs1_w), 
				.rs2(rs2_w), 
				.rd(rd_w), 
				.alu_uop(uop_w), 
				.opcode(), 
				.imm(imm_w), 
				.f7(f7_w), 
				.ctrlSig(ctrlSig_w));

register_file register_file_inst (.rd_data(rd_data_w), 
				.rs1(rs1_w), 
				.rs2(rs2_w), 
				.rd(rd_r), 
				.wen(wen_r), 
				.ren(1'b1), 
				.rst_n(rst_n),
				.o1(op1_w), 
				.o2(op2_w));

//Add to control unit
assign op2_imm_w = (i_frame | st | auipc) ? imm_w : op2_w;        //Operand 2 is imm if its I-frmae (alu/load) or store op
assign wen_w = ~(st | branch_op);		 //If branch or store instruction then dont write back to register
assign op1_pc_w = auipc ? pc_w : op1_w;


always @(*) begin
	if (branch_op) begin // for branch ops, use corresponding alu op
		case (uop_w[2:1])
			2'b00 : begin 
				alu_uop_r = 3'b000; 
				valid_f7_r = 1'b1; // eq -> do sub op
				end
			2'b10 : alu_uop_r = 3'b010; // signed lt -> signed lt -> do 
			2'b11 : alu_uop_r = 3'b011; // unsigned lt
			default : begin	
				alu_uop_r = uop_w; 
				valid_f7_r = 1'b0;
				end
		endcase
	end else if (auipc) begin
		alu_uop_r = 3'b000; //Add PC + Imm
		valid_f7_r = 1'b0;
	end else begin
		alu_uop_r = (ld | st) ? 3'b000 : uop_w;
		valid_f7_r = f7_w & (ctrlSig_w[2]  | ~ctrlSig_w[1]);
	end
end

always @(*) begin
	if (branch_op) begin	// handle branching condition base on type of alu op used (make it readable)
		branch_r = (uop_w[2]^uop_w[0]) ? ~zero_w : zero_w;
		//case ({uop[2], uop[0]})
		//	2'b00 : branch_r = zero_w;
		//	2'b01 : branch_r = ~zero_w;
		//	2'b10 : branch_r = ~zero_w;
		//	2'b11 : branch_r = zero_w;
		//endcase
	end else begin
		branch_r = 1'b0;
	end
end


alu_32 alu_inst (.op1(op1_pc_w), 
		.op2(op2_imm_w), 
		.uop(alu_uop_r), 
		.f7(valid_f7_r), 
		.rst_n(rst_n), 
		.out(alu_out_w),
		.zero(zero_w));

assign mem_addr = alu_out_w;

assign b_hbar_w = ~uop_w[0];
assign bypass_w = uop_w[1];
assign sign_w = uop_w[2];

extend32 ext32 (.data_in(data_in), .data_out(extended_data_in), .b_hbar(b_hbar_w), .bypass(bypass_w), .sig(sig_w));
assign alu_out_imm_w = lui ? imm_w : alu_out_w;
assign data_wb_w = ld ? extended_data_in : alu_out_imm_w;

assign data_out = op2_w;

//Mem access mode
always @(*) begin
	if (st & !ld) begin
		if (bypass_w) begin
			mem_access_mode_r = 2'b11;
		end else begin
			if (b_hbar_w) begin
				mem_access_mode_r = 2'b01;
			end else begin
				mem_access_mode_r = 2'b10;
			end
		end
	end else begin
		mem_access_mode_r = 2'b00;
	end
end

//can be encoded better
assign pc_mode0_w = (branch_r | jal  | ~jalr)&(~stall);
assign pc_mode1_w = (branch_r | jal | jalr)&(~stall);
assign pc_imm_w = pc_mode0_w ? imm_w : alu_out_w;
assign pc_mode_w = {pc_mode1_w, pc_mode0_w};

p_cntr pc (.clk(clk), 
		.rst_n(rst_n),
		.mode(pc_mode_w),
		.imm(pc_imm_w), 
		.pc_o(pc_w));

assign pc_o = pc_w;
assign rd_data_w = (jal | jalr)  ? pc_w + 4 : data_wb_r;

// write back
// Half cycle path, maybe be problem in timing, since ALU is constrained in Half cycle
always @(negedge clk or negedge rst_n) begin
	if (~rst_n) begin
		data_wb_r <= 0;
		rd_r <= 0;
	end else begin
		data_wb_r <= data_wb_w;
		rd_r <= rd_w;
	end
end

// Half cycle Write back logic to reg
always @(posedge clk or negedge clk or negedge rst_n) begin
	if (~rst_n ) begin
		wen_r <= 0;
	end else begin
		wen_r <= clk ? 0 : wen_w;
	end
end

// Half cycle Write back logic to mem
always @(posedge clk or negedge clk or negedge rst_n) begin
	if (~rst_n ) begin
		mem_access_mode <= 2'b00;
	end else begin
		mem_access_mode <= clk ? 2'b00 : mem_access_mode_r;
	end
end

endmodule

/*
* TODO
* 1. ctrl unit
* - Write to use ALU for load operation -> alu_uop and load ctrl signals as output
* - ID is the control unit, add other control signals, like deciding the alu_uop for diff operations in control unit (load branch etc)
* 
* 2. Proper dmem interface
* - Take a protocol, first do single cycle write, then can move to multiple cycle read writes, with stalls
*
* 3. Add branch condition (done verify, add to control unit) (tested only beq)
* eq -> zero = 1 (sub op)
* neq -> zero = 0 (sub op)
* lt/ltu -> zero = 0 (slt/sltu)
* ge/geu -> zero = 1 (slt/sltu)
* - Fix signed and unsigned comparions
* 
* 4. Modification of PC based on op (kind of works)
* 00 -> PC = PC (stall) -> bypass mode
* 01 -> PC = PC + 4 (Next instr, normal op) -> modify adder
* 11 -> PC = PC + IMM (Branch, JAL) -> modify adder
* 10 -> PC = rs1 + IMM (JALR) -> bypass mode
* -Ability to load PC in reg file (for JALR), should happen at write back stage ? yes (done)
* - Do PC+imm in alu, just bypass pc
* 
* 5. LUI, AUIPC, JAL, JALR (done)
*
* 6. Refactor code, make proper modules, load in quartus
*
* 7. Setup verification environment, moderate testing
*
* 8. Single cycle RISC-V done, document it.
*/
