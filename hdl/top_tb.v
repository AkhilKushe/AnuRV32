module top_tb();

wire [31:0] pc_w;
wire [31:0] instr_w;

wire [31:0] addr_w;
wire [31:0] data_core_mem;
wire [31:0] data_mem_core;
wire [1:0] access_mode_w;
reg clk, rst_n;

mem #(.DATA_WIDTH(32), .ADDR_WIDTH(16)) instr_mem (.addr(pc_w[15:0]),
			.data(instr_w));

data_memory dmem(.addr(addr_w), 
		.data_in(data_core_mem), 
		.en(1'b1), 
		.access_mode(access_mode_w), 
		.data_out(data_mem_core));

anu_core c1 (.stall(1'b0),
		.instr(instr_w), 
		.data_in(data_mem_core),
		.rst_n(rst_n), 
		.clk(clk), 
		.pc_o(pc_w),
		.data_out(data_core_mem),
		.mem_addr(addr_w),
		.mem_access_mode(access_mode_w));

initial 
	$readmemb(getenv("INSTR_TEST"), instr_mem.mem);

always begin
	clk = 0;
	#5;
	clk = 1;
	#5;
end

initial begin
   $dumpfile("test1");
   $dumpvars(0);
	rst_n = 1;
	#1 rst_n = 0;
	#5 rst_n = 1;
	#1000 ; $finish; 
end

endmodule
