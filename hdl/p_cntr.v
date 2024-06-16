module p_cntr (clk, rst_n, mode, imm, pc_o);
input clk;
input rst_n;
input [1:0] mode;
input [31:0] imm;
output reg [31:0] pc_o;

parameter STALL=2'b00;
parameter INCR=2'b01;
parameter BRANCH=2'b11;
parameter JALR=2'b10;

reg [31:0] pc_r;

always @(*) begin
	case (mode)
	STALL : pc_r = pc_o;
	INCR : pc_r = pc_o + 4;
	BRANCH : pc_r = pc_o + imm;
	JALR : pc_r = imm;
	endcase
end

always @(posedge clk or negedge rst_n) begin
	if (~rst_n) begin
		pc_o <= 0;
	end else begin
		pc_o <= pc_r;
	end
end

endmodule
