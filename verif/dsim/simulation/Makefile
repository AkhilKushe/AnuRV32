compile_opts= -f ../dut_file_list.f -f ../tb_file_list.f -sv -uvm 1.2 +incdir+/home/akarsh/projects/AnuRV32/verif/dsim/tb #+acc+b 
c_plus=#-waves waves.mxd 

clean: 
	rm -rf dsim* *mxd *db

run_coverage:
	dsim $(compile_opts) $(c_plus) +acc+rwcbfsWF -code-cov a 

run: 
	dsim $(compile_opts) $(c_plus)
	
coverage_report: 
	dcreport -out_dir coverage_report metrics.db