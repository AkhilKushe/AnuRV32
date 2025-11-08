class agent extends uvm_agent; 
    `uvm_component_utils(agent)

    function new (string name="agent", uvm_component parent=null); 
        super.new(name, parent);
        `uvm_info("CREATE", $sformatf("%m Agent created"), UVM_LOW)
    endfunction 

    monitor mon; 

    virtual function void build_phase(uvm_phase phase); 
        super.build_phase(phase); 
        mon = monitor::type_id::create("Monitor", this); 
    endfunction

endclass 