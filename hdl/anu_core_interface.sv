interface anu_core_interface (input bit clk); 
logic stall=1'b0;
logic [31:0] instr;
logic [31:0] data_in;
logic rst_n;

logic  [31:0] pc_o;
logic  [31:0] data_out;
logic  [31:0] mem_addr;
logic  [1:0] mem_access_mode;

modport dut (input instr); 

clocking mon @(posedge clk); 
    input  instr; 
endclocking

endinterface 