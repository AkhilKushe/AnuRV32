import uvm_pkg::*; 
import agent_pkg::*; 

class environment extends uvm_env; 
`uvm_component_utils(environment)

    function new (string name="anu_environment", uvm_component parent=null); 
        super.new(name, parent); 
        `uvm_info("CREATE",$sformatf("%m environment created"), UVM_LOW )
    endfunction
    
    agent passive_agent ; 
    
    virtual function void build_phase(uvm_phase phase); 
        super.build_phase(phase); 
        passive_agent = agent::type_id::create("passive_agent", this); 
    endfunction 

endclass 