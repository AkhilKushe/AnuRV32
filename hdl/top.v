import uvm_pkg::*; 

module top();

bit clk;
reg [31:0] mem_temp [65536-1:0]; 
anu_core_interface anu_inf(clk); 

mem #(.DATA_WIDTH(32), .ADDR_WIDTH(16)) instr_mem (.addr(anu_inf.pc_o[15:0]),
			.data(anu_inf.instr));

data_memory dmem(.addr(anu_inf.mem_addr), 
		.data_in(anu_inf.data_out), 
		.en(1'b1), 
		.access_mode(anu_inf.mem_access_mode), 
		.data_out(anu_inf.data_in));

anu_core c1 (.stall(anu_inf.stall),
		.instr(anu_inf.instr), 
		.data_in(anu_inf.data_in),
		.rst_n(anu_inf.rst_n), 
		.clk(anu_inf.clk), 
		.pc_o(anu_inf.pc_o),
		.data_out(anu_inf.data_out),
		.mem_addr(anu_inf.mem_addr),
		.mem_access_mode(anu_inf.mem_access_mode));

initial begin  
	uvm_config_db#(virtual anu_core_interface)::set(uvm_root::get(), "*", "anu_inf", anu_inf); 
	run_test("base_test");
end 

initial begin  
	$readmemb(getenv("INSTR_TEST"), instr_mem.mem);
end 

always #5 clk = ~clk;  

initial begin
//    $dumpvars();
	anu_inf.rst_n = 1;
	#1 anu_inf.rst_n = 0;
	#5 anu_inf.rst_n = 1;
	#1000 ; $display("%m" ); $finish; 
end

endmodule
