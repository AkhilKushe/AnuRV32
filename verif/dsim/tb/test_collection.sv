import uvm_pkg::*; 
class base_test extends uvm_test; 
    `uvm_component_utils(base_test)

    function new(string name = "base_test", uvm_component parent=null);
        super.new(name, parent); 
        `uvm_info("CREATE", $sformatf("%m base_test created"), UVM_MEDIUM)
    endfunction

    environment env; 
    virtual anu_core_interface core_intf; 

    virtual function void build_phase(uvm_phase phase); 
        super.build_phase(phase); 

        env = environment::type_id::create("env", this); 

        if (!uvm_config_db#(virtual anu_core_interface)::get(this, "", "anu_inf", core_intf))
            `uvm_fatal("%m", "Did not get virtual interface")
        
        // uvm_config_db#(virutal anu_core_interface )::set(this, "", "anu_inf", core_intf); 

    endfunction 

    virtual function void end_of_elaboration_phase (uvm_phase phase);
         uvm_top.print_topology ();
    endfunction

    virtual task run_phase(uvm_phase phase);     
        super.run_phase(phase); 
    endtask 

endclass