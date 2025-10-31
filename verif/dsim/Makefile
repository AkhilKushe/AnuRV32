compile_opts= -f dut_file_list.f -sv 

run_coverage:
	dsim $(compile_opts) +acc+rwcbfsWF -code-cov a 

run: 
	dsim $(compile_opts) 
	
coverage_report: 
	dcreport -out_dir coverage_report metrics.db