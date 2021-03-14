# uvm_testbench_generator
generate complete uvm_testbench using pyhton3 script


usage:
Run the command in the directory where the script exists.
python3 py3_uvm_gen.py -p project name -i list -o list 

after -p give the name of the project.
after -i give the list of active agent by space
after -o give the list of passive agent by space
    example 1: one input agent/ active agent, one output agent/passive agent:		
               python3 py3_uvm_gen.py -p spi_dv -i spi -o apb 
    example 2: two input agent/active agent:
               python3 py3_uvm_gen.py -p spi_dv -i spi -i apb

It will generate a directory named as <project>(the name after -p <project>)
inside that directory doc, rtl, dv directory will be created.
nside dv directory agent,env, sim, tb, tests directories will be created. 
