// Not required
module branch_unit ( op1,
		     op2,
		     sig,
		     lt,
		     eq);

input [31:0] op1;
input [31:0] op2;
input sig;
output lt;
output eq;

wire eq_w;
wire sig_lt_w;
wire usig_lt_w;

assign lt = sig ? sig_lt_w : usig_lt_w;
assign eq = eq_w;

// Unsigned comparison
assign usig_lt_w = op1 < op2;
assign eq_w = op1 == op2;

// Signed comparison
always @(*) begin

end

endmodule
