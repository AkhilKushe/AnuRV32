module alu_32 (op1, op2, uop, f7, rst_n, out, zero);

input [31:0] op1;
input [31:0] op2;
input [2:0] uop;
input f7;
input rst_n;
output reg [31:0]out;
output zero;

parameter ADD_SUB=3'b000;
parameter AND=3'b111;
parameter OR=3'b110;
parameter XOR=3'b100;
parameter SL=3'b001;
parameter SR=3'b101;
parameter SLT=3'b010;
parameter SLTU=3'b011;

wire signed [31:0] SR_signed ;
wire [31:0] SR_unsigned ;
assign SR_signed = $signed(op1) >>> (op2 & 32'h0000001f);
assign SR_unsigned = op1 >> (op2 & 32'h0000001f);

always @(*) begin
	if (~rst_n) begin
		out = 32'b0;
	end else begin
	case (uop)
		ADD_SUB : out = f7 ? (op1 - op2) : (op1 + op2);
		AND : out =  op1 & op2;
		OR : out = op1 | op2;
		XOR : out = op1 ^ op2;
		SL : out = op1 << (op2 & 32'h0000001f);
		SR : begin
			$display("Signed bit %d",SR_signed);
			$display("Unsigned bit %d", SR_unsigned);
			$display("f7 %d", f7);
			out = f7 ? SR_signed : SR_unsigned;
			$display("out %d", out);
		end 
		SLT : out = ( $signed(op1) < $signed(op2) );
		SLTU : out = ( op1 < op2 );
	endcase
	end
end

assign zero = ~(| out);


endmodule 
