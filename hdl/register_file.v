module register_file (rd_data, rs1, rs2, rd, wen, ren, rst_n, o1, o2);
input [31:0] rd_data;
input [4:0] rs1;
input [4:0] rs2;
input [4:0] rd;
input wen, ren, rst_n;

output reg [31:0] o1;
output reg [31:0] o2;

reg [31:0] reg_mem [31:0];

//How to handle simultanous read write ?

//read
always @(*) begin
	if (~rst_n) begin
		o1 = 32'd0;
		o2 = 32'b0;
	end else begin
		if (~ren) begin
			o1 = o1;	//Combo loops ?
			o2 = o2;
		end else begin
			o1 = reg_mem[rs1];
			o2 = reg_mem[rs2];
		end
	end
end

always @(*) begin
	reg_mem[0] = 32'd0;
end

//assign reg_mem[0] = 0;

//write back
// For modelsim
/*
always @(*) begin
	if (wen & (|rd)) begin
		reg_mem[rd] = rd_data;
	end 
end
*/
// To satisfy icarus verilog :)

genvar                i;
generate
   for (i=0; i < 32; i=i+1) begin: register_file
	  always @(*)
		if (~rst_n)
		  reg_mem[i] = 0;
		else if (wen & (|rd))
		  if (rd == i)
			reg_mem[i] = rd_data;
	 end
endgenerate

endmodule
