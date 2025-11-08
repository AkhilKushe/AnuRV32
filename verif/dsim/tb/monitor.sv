class monitor extends uvm_monitor; 
    `uvm_component_utils(monitor)

    function new (string name="monitor", uvm_component parent=null); 
        super.new(name, parent); 
        `uvm_info("CREATE", $sformatf("%m Created Monitor"), UVM_LOW)
    endfunction 

    virtual anu_core_interface vif; 
    logic [31:0] instr_read; 

    virtual function void build_phase(uvm_phase phase); 
        super.build_phase(phase); 

        if (!uvm_config_db#(virtual anu_core_interface)::get(this, "", "anu_inf", vif))
            `uvm_fatal("%m", "Did not get interface")
        `uvm_info("BUILD", $sformatf("%m Built monitor "), UVM_LOW)
    endfunction 

    virtual task run_phase(uvm_phase phase); 
        super.run_phase(phase); 
        phase.raise_objection(this); 
        `uvm_info("RUN", $sformatf("%m runphase monitor "), UVM_LOW)
        // phase.drop_objection(this); 
        forever begin 
            @(vif.mon); 
            instr_read = vif.mon.instr; 
            // phase.raise_objection(this); 
            `uvm_info("RUN", $sformatf("%m runphase monitor inside forever "), UVM_LOW)
            `uvm_info("MONITOR", $sformatf("%h" , instr_read), UVM_MEDIUM)
            // phase.drop_objection(this); 
        end
    endtask
endclass 
