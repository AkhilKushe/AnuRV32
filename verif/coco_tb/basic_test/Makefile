#SIM ?= icarus
SIM ?= verilator
TOPLEVEL_LANG ?= verilog

VERILOG_INCLUDE_DIRS += $(PWD)/../../../hdl/
VERILOG_SOURCES += $(PWD)/../../../hdl/anu_core.v
VERILOG_SOURCES += $(PWD)/../../../hdl/alu.v
VERILOG_SOURCES += $(PWD)/../../../hdl/ID.v
VERILOG_SOURCES += $(PWD)/../../../hdl/extend32.v
VERILOG_SOURCES += $(PWD)/../../../hdl/memory.v
VERILOG_SOURCES += $(PWD)/../../../hdl/p_cntr.v
VERILOG_SOURCES += $(PWD)/../../../hdl/register_file.v
VERILOG_SOURCES += $(PWD)/../../../hdl/branch_unit.v
VERILOG_SOURCES += $(PWD)/../../../hdl/control_unit.v
#VERILOG_SOURCES += $(PWD)/../../../hdl/top_tb.v

MODULE=test_1 
TOPLEVEL=anu_core

EXTRA_ARGS += --trace --Wno-lint --coverage --cc --timing --Wno-ALWNEVER

COCOTB_LOG_LEVEL=DEBUG 
COCOTB_SCHEDULER_DEBUG=1

#cntr :
#	$(MAKE) sim
include $(shell cocotb-config --makefiles)/Makefile.sim