module alu_32 (op1, op2, uop, f7, rst_n, out, zero);

input [31:0] op1;
input [31:0] op2;
input [2:0] uop;
input f7;
input rst_n;
output reg [31:0]out;
output zero;

parameter ADD_SUB=3'b000;
parameter AND=3'b100;
parameter OR=3'b110;
parameter XOR=3'b111;
parameter SL=3'b001;
parameter SR=3'b101;
parameter SLT=3'b010;
parameter SLTU=3'b011;

always @(*) begin
	if (~rst_n) begin
		out = 32'b0;
	end else begin
	case (uop)
		ADD_SUB : out = f7 ? (op1 - op2) : (op1 + op2);
		AND : out =  op1 & op2;
		OR : out = op1 | op2;
		XOR : out = op1 ^ op2;
		SL : out = op1 << op2;
		SR : out = f7 ? (op1 >>> op2) : (op1 >> op2);
		SLT : begin
			// Is the signed comparison correct ? Verify !!!!!
			if (op1[31]==op2[31]) begin
				out = (op1 < op2);
			end else begin
				out = {31'd0, op1[31]};
			end
		      end
		SLTU : out = ( op1 < op2 );
	endcase
	end
end

assign zero = ~(| out);


endmodule 
