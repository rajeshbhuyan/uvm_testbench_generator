#!usr/bin/python
##
##-------------------------------------------------
## geneate a uvm testbench #####
## The directory structure is is as follows. top/test/env/agent/seq/seqer/driver/monitor/interface, scb/refm/cov/assertion/seqlib
##project
# ***********************************************************************
# ***********************************************************************
# PROJECT        : uvm generator using python3
# FILENAME       : py3_uvm_gen.py
# Author         : [rajeshb@perfectvips.com]
# CREATED        : Sun Mar 14 09:39:50 2021
# LAST MODIFIED  : Sun Mar 14 09:39:50 2021
# ***********************************************************************
# DESCRIPTION    :
# ***********************************************************************
# $Revision: $ 1.0
# ***********************************************************************
#--------------------------------------------------
import re
import sys
import os
import getopt
import datetime

def usage():
    print  ("	********USAGE: python py3_uvm_gen.py -help/h (print this message)********\n" )
    print  ("	this scritps support several input agent, output agent, agent with ral" )
    print  ("	for the ral agent, support adapter for i2c/spi/apb/ahb,not support yet." )
    print  ("	python3 py3_uvm_gen.py -p project name -i list (input agent name)/active -o list (output agent name)/passive -r register agent with ral\n") 
    print  ("	example 1: one input agent, one output agent,one ral agent:\n		python3 py3_uvm_gen.py -p proj_1 -i spi -o apb -r wishbone\n") 
    print  ("	example 2: two input agent:\n 		                              python3 py3_uvm_gen.py -p proj_2 -i uart apb\n") 
    print  ("	example 3: two input agent, one output agent,two ral agent:\n 		python3 py3_uvm_gen.py -p proj_3 -i i2c uart -o apb -r wishbone ahb\n") 
    print  ("	********************************************************************\n") 

def tb_gen(argv):
    global project    
    global tbname     
    global envname    
    global agent_name 
    global agent_if   
    global agent_item 
    global agent_list
    global name
    global email
    name="Rajesh Kumar Bhuyan"
    email="rajeshb@perfectvips.com"
    mode = "irun"
    i_agt=[]
    o_agt=[]

    try:
        opts, args = getopt.getopt(argv, "p:i:i:o:runvcs", ["project", "agent"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            usage()
            sys.exit()

        elif opt in("-p", "project"):
            project = arg
        elif opt in("-i"):
            agent_name = arg
            i_agt.append(arg)
        elif opt in("-o"):
            o_agt.append(arg)
        elif opt in("-irun"):
            mode = "irun" 
        elif opt in("-vcs"):
            mode = "vcs" 

    tbname = project 
    envname = project+"_env"
    agent_list = i_agt + o_agt

    print ("The project name is", project)
    print ("The agent name is"  , agent_name)
    print ("The simulator is "  , mode)
    print ("\nParsing  Input Agent ...\n\n")
    print ("Writing code to files")
    if os.path.exists(project+"/doc/") != True:
        os.makedirs(project+"/doc/")

    if os.path.exists(project+"/rtl/") != True:
        os.makedirs(project+"/rtl/")

    if os.path.exists(project+"/dv/env/")!= True:
        os.makedirs(project+"/dv/env/")

    if os.path.exists(project+"/dv/tb/")!= True:
        os.makedirs(project+"/dv/tb/")

    if os.path.exists(project+"/dv/sim/")!= True:
        os.makedirs(project+"/dv/sim/")
    #os.makedirs(project+"/dv/tests/")
    if os.path.exists(project+"/dv/tests/test_seq") != True :
        os.makedirs(project+"/dv/tests/test_seq")

    template_type = "act"
    for agt in i_agt:
        if os.path.exists(project+"/dv/agent/"+agt)!= True:
            os.makedirs(project+"/dv/agent/"+agt)
        #create the agent files
        agent_name = agt
        agent_if = agent_name+"_if"
        agent_item = agent_name+"_seq_item"
        gen_if() 
        gen_seq_item() 
        gen_config(template_type) 
        if(template_type == "act"): 
            gen_driver() 
            gen_seq() 
            gen_sequencer() 

        gen_monitor() 
        gen_agent(template_type) 
        gen_agent_pkg(template_type) 
    template_type = "pas"
    for agt in o_agt:
        if os.path.exists(project+"/dv/agent/"+agt)!= True:
            os.makedirs(project+"/dv/agent/"+agt)
        #create the agent files
        agent_name = agt
        agent_if = agent_name+"_if"
        agent_item = agent_name+"_seq_item"
        gen_if() 
        gen_seq_item() 
        gen_config(template_type) 
        #if(template_type == "act"): 
        #    gen_driver() 
        #    gen_seq() 
        #    gen_sequencer() 
        gen_monitor() 
        gen_agent(template_type) 
        gen_agent_pkg(template_type) 
    # gen_cov() 
    gen_refm()
    gen_scb()

    # gen_tb();
    # gen_test();
    gen_top_test();
    gen_top()
    gen_top_config()
    gen_top_env()
    gen_top_pkg()

    #gen_questa_script();
    if mode == "irun":
        gen_irun_script()
    else:
        gen_vcs_script()


def write_file_header(file_f):
    #f = open(file_f, "w")
    #old = f.read()
    #f.seek(0)
    # name="Rajesh Kumar Bhuyan"
    email = "rajeshb@perfectvips.com"
    date  =  datetime.datetime.now() #str(os.system("date"))
    print(date)
    print(file_f)
    print ("//=============================================================================", file=file_f)
    print ("// copyright", file=file_f) 
    print ("//=============================================================================", file=file_f) 
    print ("// Project  : ",file=file_f) # + project + file=file_f) 
    print ("// File Name: $fname", file=file_f) 
    print ("// Author   : Name   : "+name+ "",file=file_f) 
    print ("//            Email  : "+email+ "", file=file_f) 
    print ("// Created  : ",date, file=file_f) 
    print ("//            Dept   : $dept", file=file_f) 
    print ("// Version  : $version", file=file_f) 
    print ("//=============================================================================", file=file_f) 
    print ("// Description:", file=file_f) 
    print ("//=============================================================================\n", file=file_f) 
#end def write_file_header


def gen_if(): 
    global project

    dir_path = project+"/dv/agent/"+agent_name+"/"
    try:
        if_f = open( dir_path+agent_name+"_if.sv","w" )
    except IOError:
        print ("Exiting due to Error: can't open interface: "+agent_name )

    write_file_header(if_f)
    print    ("`ifndef "+agent_name.upper()+"_IF_SV" , file=if_f)
    print    ("`define "+agent_name.upper()+"_IF_SV\n" , file=if_f)

    print    ("interface "+agent_if+"(); \n" , file=if_f)

    print    ("  // You could add properties and assertions, for example" , file=if_f)
    print    ("  // property name " , file=if_f)
    print    ("  // ..." , file=if_f)
    print    ("  // endproperty : name" , file=if_f)
    print    ("  // label: assert property(name) \n" , file=if_f)

    print    ("endinterface : "+agent_if+"\n" , file=if_f)
    print    ("`endif // "+agent_name.upper()+"_IF_SV" , file=if_f)
    if_f.close( ) 
#end gen_if


def gen_seq_item():
    global project

    dir_path = project+"/dv/agent/"+agent_name+"/"
    try:
        tr_f = open( dir_path+agent_item+".sv", "w" )
    except IOError:
        print ("Exiting due to Error: can't open data_item: "+agent_item)

    write_file_header(tr_f)
    print  ("`ifndef " +agent_item.upper()+"_SV",file=tr_f)
    print  ("`define " +agent_item.upper()+"_SV\n",file=tr_f)

    print  ("class "+agent_item+" extends uvm_sequence_item; ",file=tr_f)
    print  ("  `uvm_object_utils("+agent_item+")\n;",file=tr_f)
    print  ("  extern function new(string name = file=\""+agent_item+"\");\n",tr_f)

    print  ("endclass : "+agent_item+" file=\n",tr_f)

    print  ("function "+agent_item+"::new(string name = file=\""+agent_item+"\");",tr_f)
    print  ("  file=super.new(name);",tr_f)
    print  ("endfunction : file=new\n",tr_f)

    print  ("`endif // "+agent_item.upper()+"_SV\n",file=tr_f)
    tr_f.close()
#end gen_data_item


def gen_config(template_type):
    global project

    dir_path = project+"/dv/agent/"+agent_name+"/"

    print ("type = $template_type,   agent name = " + agent_name + "\n") #;)
    try:
        cfg_f = open(dir_path+agent_name+"_agent_config.sv", "w")
    except IOError:
        print ("Exiting due to Error: can't open config: "+agent_name)
    write_file_header(cfg_f)

    print  ("`ifndef " +agent_name.upper()+"_AGENT_CONFIG_SV;", file=cfg_f)
    print  ("`define " +agent_name.upper()+"_AGENT_CONFIG_SV\n;", file=cfg_f)

    print  ("class "+agent_name+"_agent_config extends uvm_object;", file=cfg_f)
      
    print  ("  `uvm_object_utils("+agent_name+"_agent_config)\n;", file=cfg_f)
    if(template_type == "pas"):
        print  ("  rand uvm_active_passive_enum is_active = UVM_PASSIVE;\n", file=cfg_f)
    else:
        print  ("  rand uvm_active_passive_enum is_active = UVM_ACTIVE;\n", file=cfg_f)

    print  ("  rand bit coverage_enable = 0;", file=cfg_f)
    print  ("  rand bit checks_enable = 0;", file=cfg_f)

    print  ("  extern function new(string name = \""+agent_name+"\_agent_config\");\n", file=cfg_f)

    print  ("endclass : "+agent_name+"_agent_config \n", file=cfg_f)
    print  ("function "+agent_name+"_agent_config::new(string name = \""+agent_name+"\_agent_config\");", file=cfg_f)
    print  ("  super.new(name);", file=cfg_f)
    print  ("endfunction : new\n", file=cfg_f)

    print  ("`endif // " +agent_name.upper()+"_AGENT_CONFIG_SV\n", file=cfg_f)
    cfg_f.close()
##end gen_config


def gen_driver():
    global project

    dir_path = project+"/dv/agent/"+agent_name+"/"
    try:
        drv_f = open(dir_path+agent_name+"_driver.sv", "w" )
    except IOError:
        print ("Exiting due to Error: can't open driver: "+agent_name)

    write_file_header(drv_f)

    print  ("`ifndef "+agent_name.upper()+"_DRIVER_SV",file=drv_f)
    print  ("`define "+agent_name.upper()+"_DRIVER_SV\n",file=drv_f)

    print  ("class "+agent_name+"_driver extends uvm_driver #("+agent_item+");", file=drv_f)
    print  ("  `uvm_component_utils("+agent_name+"_driver)\n",file=drv_f)

    print  ("  virtual interface  "+agent_if+" vif;\n",file=drv_f)

    print  ("  extern function new(string name, uvm_component parent);",file=drv_f)
    print  ("  extern virtual function void build_phase (uvm_phase phase);",file=drv_f)
    print  ("  extern virtual function void connect_phase(uvm_phase phase);", file=drv_f)
    print  ("  extern task main_phase(uvm_phase phase);",file=drv_f)
    print  ("  extern task do_drive("+agent_item+" req);\n",file=drv_f)
    print  ("endclass : "+agent_name+"_driver\n",file=drv_f)

    print  ("function "+agent_name+"_driver::new(string name, uvm_component parent);",file=drv_f)
    print  ("  super.new(name, parent);",file=drv_f)
    print  ("endfunction : new\n",file=drv_f)

    print  ("function void "+agent_name+"_driver::build_phase(uvm_phase phase);",file=drv_f)
    print  ("  super.build_phase(phase);",file=drv_f)
    print  ("endfunction : build_phase\n",file=drv_f)

    print  ("function void "+agent_name+"_driver::connect_phase(uvm_phase phase);",file=drv_f)
    print  ("  super.connect_phase(phase);\n",file=drv_f)
    print  ("  if (!uvm_config_db #(virtual "+agent_name+'_if)::get(this, "*", "' +agent_name+"_vif\", vif))",file=drv_f)
    print  ("    `uvm_error(\"NOVIF\", {\"virtual interface must be set for: \",get_full_name(),\".vif\"})\n",file=drv_f)
    print  ("endfunction : connect_phase\n",file=drv_f)

    print  ("task "+agent_name+"_driver::main_phase(uvm_phase phase);",file=drv_f)
    #print >>drv_f, "  super.run_phase(phase);\n"
    print  ("  `uvm_info(get_type_name(), \"main_phase\", UVM_HIGH)\n",file=drv_f)
    print  ("  forever",file=drv_f)
    print  ("  begin",file=drv_f)
    print  ("    seq_item_port.get_next_item(req);\n",file=drv_f)
    print  ("      `uvm_info(get_type_name(), {\"req item\\n\",req.sprint}, UVM_HIGH)\n",file=drv_f)
    print  ("    do_drive(req);\n",file=drv_f)
    print  ("    //$cast(rsp, req.clone());",file=drv_f)
    print  ("    seq_item_port.item_done();",file=drv_f)
    print  ("    # 10ns;\n",file=drv_f)
    print  ("  end\n",file=drv_f)
    print  ("endtask : main_phase\n",file=drv_f)

    print  ("task "+agent_name+"_driver::do_drive("+agent_item+" req);\n\n",file=drv_f)
    print  ("endtask : do_drive\n",file=drv_f)

    print  ("`endif // "+agent_name.upper()+"_DRIVER_SV\n\n",file=drv_f)
    drv_f.close();
#end def gen_driver


def gen_monitor(): 
    global project
    
    dir_path = project+"/dv/agent/"+agent_name+"/"
    try:
        mon_f = open( dir_path+agent_name+"_monitor.sv", "w" )
    except IOError:
        print ("Exiting due to Error: can't open monitor: "+agent_name)
#
#    write_file_header ""+agent_name+"_monitor.sv", "Monitor for "+agent_name+""
    write_file_header(mon_f)
    print  ("`ifndef "+agent_name.upper()+"_MONITOR_SV", file=mon_f)
    print  ("`define "+agent_name.upper()+"_MONITOR_SV\n", file=mon_f)

    print  ("class "+agent_name+"_monitor extends uvm_monitor;", file=mon_f)
    print  ("  `uvm_component_utils("+agent_name+"_monitor)\n", file=mon_f)
    print  ("  virtual interface  "+agent_if+" vif;\n", file=mon_f)
    print  ("  uvm_analysis_port #("+agent_item+") analysis_port;\n", file=mon_f)

    print  ("  "+agent_item+" m_trans;\n", file=mon_f)

    print  ("  extern function new(string name, uvm_component parent);", file=mon_f)
    print  ("  extern virtual function void build_phase (uvm_phase phase);", file=mon_f)
    print  ("  extern virtual function void connect_phase(uvm_phase phase);"    , file=mon_f)
    print  ("  extern task main_phase(uvm_phase phase);", file=mon_f)
    print  ("  extern task do_mon();\n", file=mon_f)

    print  ("endclass : "+agent_name+"_monitor \n", file=mon_f)
    print  ("function "+agent_name+"_monitor::new(string name, uvm_component parent);\n", file=mon_f)
    print  ("  super.new(name, parent);", file=mon_f)
    print  ("  analysis_port = new(\"analysis_port\", this);\n", file=mon_f)
    print  ("endfunction : new\n", file=mon_f)

    print  ("function void "+agent_name+"_monitor::build_phase(uvm_phase phase);\n", file=mon_f)
    print  ("  super.build_phase(phase);\n", file=mon_f)
    print  ("endfunction : build_phase\n", file=mon_f)

    print  ("function void "+agent_name+"_monitor::connect_phase(uvm_phase phase);", file=mon_f)
    print  ("  super.connect_phase(phase);\n", file=mon_f)
    print  ("  if (!uvm_config_db #(virtual "+agent_name+'_if)::get(this, "*", "' +agent_name+"_vif\", vif))", file=mon_f)
    #print  ("  if (!uvm_config_db #(virtual "+agent_name+')::get(this, "",' +agent_name+"_vif, vif))", file=mon_f)
    print  ("    `uvm_error(\"NOVIF\",{\"virtual interface must be set for: \",get_full_name(),\".vif\"})\n", file=mon_f)
    print  ("endfunction : connect_phase\n", file=mon_f)

    print  ("task "+agent_name+"_monitor::main_phase(uvm_phase phase);", file=mon_f)
    print  ("  `uvm_info(get_type_name(), \"main_phase\", UVM_HIGH)\n", file=mon_f)
    print  ("  m_trans = "+agent_item+"::type_id::create(\"m_trans\");", file=mon_f)
    print  ("  do_mon();\n", file=mon_f)
    print  ("endtask : main_phase\n", file=mon_f)

    print  ("task "+agent_name+"_monitor::do_mon();\n", file=mon_f)
    print  ("endtask : do_mon\n", file=mon_f)

    print  ("`endif // "+agent_name.upper()+"_MONITOR_SV\n\n", file=mon_f)
    mon_f.close();
 #end def gen_monitor 


def gen_sequencer(): 
    global project

    dir_path = project+"/dv/agent/"+agent_name+"/"
    try:
        sqr_f = open(dir_path+agent_name+"_sequencer.sv", "w" )
    except IOError:
        print ("Exiting due to Error: can't open sequencer: "+agent_name)

    write_file_header(sqr_f)

    print  ("`ifndef "+agent_name.upper()+"_SEQUENCER_SV", file=sqr_f)
    print  ("`define "+agent_name.upper()+"_SEQUENCER_SV\n", file=sqr_f)

    print  ("class "+agent_name+"_sequencer extends uvm_sequencer #("+agent_item+");", file=sqr_f)
    print  ("  `uvm_component_utils("+agent_name+"_sequencer)\n", file=sqr_f)

    print  ("  extern function new(string name, uvm_component parent);\n", file=sqr_f)

    print  ("endclass : "+agent_name+"_sequencer \n", file=sqr_f)

    print  ("function "+agent_name+"_sequencer::new(string name, uvm_component parent);\n", file=sqr_f)
    print  ("  super.new(name, parent);\n", file=sqr_f)
    print  ("endfunction : new\n", file=sqr_f)

    print  ("`endif // "+agent_name.upper()+"_SEQUENCER_SV\n\n", file=sqr_f)
    sqr_f.close();
#end def gen_sequencer


def gen_agent(template_type):
    global project

    dir_path = project+"/dv/agent/"+agent_name+"/"

    try:
        agt_f = open(dir_path+agent_name+"_agent.sv", "w")
    except IOError:
        print ("Exiting due to Error: can't open sequencer: "+agent_name)
    write_file_header(agt_f)

    print   ("`ifndef " +agent_name.upper()+ "_AGENT_SV" , file=agt_f)
    print   ("`define " +agent_name.upper()+ "_AGENT_SV\n" , file=agt_f)

    print   ("class "+agent_name+"_agent extends uvm_agent;" , file=agt_f)
    print   ("  "+agent_name+"_agent_config       m_cfg;" , file=agt_f)
    if(template_type == "act"):
        print   ("  "+agent_name+"_sequencer          m_sequencer;" , file=agt_f)
        print   ("  "+agent_name+"_driver             m_driver;" , file=agt_f)

    print   ("  "+agent_name+"_monitor            m_monitor;\n" , file=agt_f)

    print   ("  uvm_analysis_port #("+agent_item+") analysis_port;\n" , file=agt_f)
    print   ("  `uvm_component_utils_begin("+agent_name+"_agent)" , file=agt_f)
    print   ("     `uvm_field_enum(uvm_active_passive_enum, is_active, UVM_DEFAULT)" , file=agt_f)
    print   ("     `uvm_field_object(m_cfg, UVM_DEFAULT | UVM_REFERENCE)" , file=agt_f)
    print   ("  `uvm_component_utils_end\n" , file=agt_f)

    print   ("  extern function new(string name, uvm_component parent); \n" , file=agt_f)
    print   ("  extern function void build_phase(uvm_phase phase);" , file=agt_f)
    print   ("  extern function void connect_phase(uvm_phase phase);\n" , file=agt_f)

    print   ("endclass : "+agent_name+"_agent" , file=agt_f)
    print   ("\n" , file=agt_f)

    print   ("function  "+agent_name+"_agent::new(string name, uvm_component parent);" , file=agt_f)
    print   ("  super.new(name, parent);" , file=agt_f)
    print   ("  analysis_port = new(\"analysis_port\", this);" , file=agt_f)
    print   ("endfunction : new" , file=agt_f)
    print   ("\n" , file=agt_f)

    print   ("function void "+agent_name+"_agent::build_phase(uvm_phase phase);" , file=agt_f)
    print   ("  super.build_phase(phase);\n" , file=agt_f)
    print   ("  if(m_cfg == null) begin" , file=agt_f)
    print   ("    if (!uvm_config_db#("+agent_name+"_agent_config)::get(this, \"\", \"m_cfg\", m_cfg))\n    begin" , file=agt_f)
    print   ("      `uvm_warning(\"NOCONFIG\", \"Config not set for Rx agent, using default is_active field\")" , file=agt_f)
    print   ("      m_cfg = "+agent_name+"_agent_config  ::type_id::create(\"m_cfg\", this);" , file=agt_f)
    print   ("    end" , file=agt_f)
    print   ("  end" , file=agt_f)
    print   ("  is_active = m_cfg.is_active;\n" , file=agt_f)

    print   ("  m_monitor     = "+agent_name+"_monitor    ::type_id::create(\"m_monitor\", this);" , file=agt_f)
    if( template_type == "act"):
        print   ("  if (is_active == UVM_ACTIVE)" , file=agt_f)
        print   ("  begin" , file=agt_f)
        print   ("    m_driver    = "+agent_name+"_driver     ::type_id::create(\"m_driver\", this);" , file=agt_f)
        print   ("    m_sequencer = "+agent_name+"_sequencer  ::type_id::create(\"m_sequencer\", this);" , file=agt_f)
        print   ("  end" , file=agt_f)
    print   ("endfunction : build_phase" , file=agt_f)
    print   ("\n" , file=agt_f)
    
    print   ("function void "+agent_name+"_agent::connect_phase(uvm_phase phase);" , file=agt_f)
    print   ("  super.connect_phase(phase);\n" , file=agt_f)
    print   ("  m_monitor.analysis_port.connect(analysis_port);" , file=agt_f)
    if( template_type == "act"):
        print   ("  if (is_active == UVM_ACTIVE)" , file=agt_f)
        print   ("  begin" , file=agt_f)
        print   ("    m_driver.seq_item_port.connect(m_sequencer.seq_item_export);" , file=agt_f)
        print   ("  end" , file=agt_f)

    print   ("endfunction : connect_phase\n" , file=agt_f)
    print   ("`endif // "+agent_name.upper()+"_AGENT_SV\n\n" , file=agt_f)
    agt_f.close()


def gen_seq(): 
    global project

    dir_path = project+"/dv/tests/test_seq/"
    try:
        seq_f = open( dir_path+agent_name+"_seq.sv", "w" )
    except IOError:
        print ("Exiting due to Error: can't open seq: "+agent_name)
    write_file_header(seq_f)

    print  ("`ifndef "+agent_name.upper()+"_SEQ_SV",file=seq_f)
    print  ("`define "+agent_name.upper()+"_SEQ_SV\n",file=seq_f)

    print  ("class "+agent_name+"_base_seq extends uvm_sequence file=#("+agent_item+");",seq_f)
    print  ("  `uvm_object_utils("+agent_name+"_base_seq)\n",file=seq_f)

    print  ("  function new(string name = file=\""+agent_name+"_base_seq\");",seq_f)
    print  ("    file=super.new(name);",seq_f)
    print  ("  file=endfunction\n",seq_f)
    print  ("  virtual task file=pre_body();",seq_f)
    print  ("    if (starting_phase != file=null)\n",seq_f)
    print  ("    starting_phase.raise_objection(this, {\"Running sequence file='\",",seq_f)
    print  ("                                          get_full_name(), file=\"'\"});\n",seq_f)
    print  ("  file=endtask\n",seq_f)
    print  ("  virtual task file=post_body();",seq_f)
    print  ("    if (starting_phase != file=null)",seq_f)
    print  ("    starting_phase.drop_objection(this, {\"Completed sequence file='\",",seq_f)
    print  ("                                         get_full_name(), file=\"'\"});\n",seq_f)
    print  ("  file=endtask\n",seq_f)
    print  ("endclass : "+agent_name+"_base_seq\n",file=seq_f)
    print  ("//-------------------------------------------------------------------------\n", file=seq_f)
    
    print  ("class "+agent_name+"_seq extends "+agent_name+"_base_seq;", file=seq_f)
    print  ("  `uvm_object_utils("+agent_name+"_seq)\n",file=seq_f)

    print  ("  extern function new(string name = file=\""+agent_name+"\_seq\");\n",file=seq_f)
    print  ("  extern task file=body();\n",file=seq_f)
    print  ("endclass : "+agent_name+"_seq\n",file=seq_f)

    print  ("function "+agent_name+"_seq::new(string name = file=\""+agent_name+"_seq\");",file=seq_f)
    print  ("  super.new(name);",file=seq_f)
    print  ("endfunction : new\n",file=seq_f)

    print  ("task "+agent_name+"_seq::body();\n",file=seq_f)
    print  ("  `uvm_info(get_type_name(), \"Default sequence starting\", file=UVM_HIGH)\n\n",file=seq_f)
    print  ("  req = "+agent_item+"::type_id::create(\"req\");\n",file=seq_f)
    print  ("  start_item(req); \n",file=seq_f)
    print  ("  if ( !req.randomize() )",file=seq_f)
    print  ("    `uvm_error(get_type_name(), \"Failed to randomize transaction\")",file=seq_f)
    print  ("  finish_item(req); \n",file=seq_f)
    print  ("  `uvm_info(get_type_name(), \"Default sequence completed\", UVM_HIGH)\n",file=seq_f)
    print  ("endtask : body\n",file=seq_f)

    print  ("`endif // "+agent_name.upper()+"_SEQ_LIB_SV\n",file=seq_f)

    seq_f.close()
#end def gen_seq


def gen_agent_pkg(template_type):
    global project

    dir_path = project+"/dv/agent/"+agent_name+"/"
    try:
        agt_pkg_f = open( dir_path+agent_name+"_pkg.sv", "w" )
    except IOError:
        print ("Exiting due to Error: can't open include file: "+agent_name)
    write_file_header(agt_pkg_f)

    print  ("`ifndef "+agent_name.upper()+"_PKG_SV", file=agt_pkg_f)
    print  ("`define "+agent_name.upper()+"_PKG_SV\n", file=agt_pkg_f)

    print  ("package "+agent_name+"_pkg;\n", file=agt_pkg_f)
    print  ("  import uvm_pkg::*;\n", file=agt_pkg_f)
    print  ("  `include \"uvm_macros.svh\"", file=agt_pkg_f)
    print  ("  `include \""+agent_item+".sv\"", file=agt_pkg_f)
    print  ("  `include \""+agent_name+"_agent_config.sv\"", file=agt_pkg_f)
    print  ("  `include \""+agent_name+"_monitor.sv\"", file=agt_pkg_f)

    if(template_type == "act"):
        print  ("  `include \""+agent_name+"_driver.sv\"\n", file=agt_pkg_f)
        print  ("  `include \""+agent_name+"_sequencer.sv\"", file=agt_pkg_f)
        #print  ("  `include \""+agent_name+"_coverage.sv\"\n", file=agt_pkg_f)
        print  ("  `include \""+agent_name+"_seq.sv\"\n", file=agt_pkg_f)

    print  ("  `include \""+agent_name+"_agent.sv\"\n", file=agt_pkg_f)
    print  ("endpackage : "+agent_name+"_pkg\n", file=agt_pkg_f)
    print  ("`endif // "+agent_name.upper()+"_PKG_SV\n", file=agt_pkg_f)

    agt_pkg_f.close();
#end def gen_agent_pkg

def gen_top_config():
    global project
    global envname

    dir_path = project+"/dv/env/"
    try:
        env_cfg_f = open( dir_path+envname+"_config.sv", "w" )
    except IOError:
        print ("Exiting due to Error: can't open config: "+envname)
    write_file_header(env_cfg_f)

    print  ("`ifndef "+envname.upper()+"_CONFIG_SV",file=env_cfg_f)
    print  ("`define "+envname.upper()+"_CONFIG_SV\n",file=env_cfg_f)

    print  ("class "+envname+"_config extends uvm_object;",file=env_cfg_f)
    print  ("  `uvm_object_utils("+envname+"_config)\n",file=env_cfg_f)
    print  ("  extern function new(string name = \""+envname+"_config\");\n",file=env_cfg_f)
    print  ("endclass : "+envname+"_config \n",file=env_cfg_f)

    print  ("function "+envname+"_config::new(string name = \""+envname+"_config\");",file=env_cfg_f)
    print  ("  super.new(name);",file=env_cfg_f)
    print  ("endfunction : new\n",file=env_cfg_f)

    print  ("`endif // "+envname.upper()+"_CONFIG_SV\n",file=env_cfg_f)
    env_cfg_f.close()
#end def gen_top_config


def gen_refm():
    global project
    global tbname

    dir_path = project+"/dv/env/"
    try:
        ref_f = open(dir_path+tbname+"_refm.sv", "w" )
    except IOError:
        print ("Exiting due to Error: can't open file: $tbname")
    write_file_header(ref_f)

    print  ("`ifndef " +tbname.upper()+"_REFM_SV",file=ref_f)
    print  ("`define " +tbname.upper()+"_REFM_SV\n",file=ref_f)

    print  ("class "+tbname+"_refm extends uvm_component;",file=ref_f)
    print  ("  `uvm_component_utils("+tbname+"_refm)\n",file=ref_f)
    print  ("//    uvm_analysis_imp#(uart_seq_item) uart_imp;\n",file=ref_f)
    print  ("  extern function new(string name, uvm_component parent);",file=ref_f)
    print  ("  extern task main_phase(uvm_phase phase);\n",file=ref_f)

    print  ("endclass : " +tbname+"_refm \n",file=ref_f)
    print  ("function "+tbname+"_refm::new(string name, uvm_component parent);\n",file=ref_f)
    print  ("  super.new(name, parent);\n",file=ref_f)
    print  ("endfunction : new\n",file=ref_f)

    print  ("task "+tbname+"_refm::main_phase(uvm_phase phase);\n\n",file=ref_f)
    print  ("endtask : main_phase\n",file=ref_f)
    print  ("`endif // "+tbname.upper()+"_REFM_SV\n\n",file=ref_f)
    ref_f.close();
#end def gen_refm

def gen_scb():
    global project
    global tbname

    dir_path = project+"/dv/env/"
    try:
        scb_f = open(dir_path+tbname+"_scb.sv", "w" )
    except IOError:
        print ("Exiting due to Error: can't open file: $tbname")

    write_file_header(scb_f)

    print  ("`ifndef "+tbname.upper()+"_SCB_SV",file=scb_f)
    print  ("`define "+tbname.upper()+"_SCB_SV\n",file=scb_f)

    print  ("class "+tbname+"_scb extends file=uvm_component;",scb_f)
    print  ("  `uvm_component_utils(" +tbname+"_scb)\n",scb_f)
    print  ("  extern function new(string name, uvm_component file=parent);",scb_f)
    print  ("  extern task main_phase(uvm_phase file=phase);\n",scb_f)
    print  ("endclass : "+tbname+"_scb file=\n",scb_f)

    print  ("function "+tbname+"_scb::new(string name, uvm_component file=parent);",scb_f)
    print  ("  super.new(name, file=parent);",scb_f)
    print  ("endfunction : file=new\n",scb_f)

    print  ("task "+tbname+"_scb::main_phase(uvm_phase file=phase);\n",scb_f)
    print  ("endtask : file=main_phase\n\n",scb_f)
    print  ("`endif // " +tbname.upper()+"_SCB_SV",scb_f)
    scb_f.close();
#end def gen_scb



def gen_top_env():
    global project
    global tbname

    dir_path = project+"/dv/env/"
    try:
        env_f = open(dir_path+tbname+"_env.sv", "w" )
    except IOError:
        print ("Exiting due to Error: can't open file: $tbname")

    write_file_header(env_f)

    print  ("`ifndef "+tbname.upper()+"_ENV_SV",file=env_f)
    print  ("`define "+tbname.upper()+"_ENV_SV\n",file=env_f)

    print  ("class "+tbname+"_env extends uvm_env;\n",file=env_f)
    print  ("  `uvm_component_utils("+tbname+"_env)\n",file=env_f)
    for  agent in agent_list:
        print  ("  "+agent+"_agent m_"+agent+"_agent; \n",file=env_f)
    #print  tbname+("_refm m_"+tbname+"_refm; file=\n",env_f)
    #print  tbname+("_scb m_"+tbname+"_scb; file=\n",env_f)

    print  ("  extern function new(string name, uvm_component parent);",file=env_f)
    print  ("  extern function void build_phase(uvm_phase phase);",file=env_f)
    print  ("  extern function void connect_phase(uvm_phase phase);",file=env_f)
    print  ("  extern function void end_of_elaboration_phase(uvm_phase phase);\n",file=env_f)

    print  ("endclass : "+tbname+"_env \n",file=env_f)

    print  ("function "+tbname+"_env::new(string name, uvm_component parent);\n",file=env_f)
    print  ("  super.new(name, parent);\n",file=env_f)
    print  ("endfunction : new\n",file=env_f)

    print  ("function void "+tbname+"_env::build_phase(uvm_phase phase);",file=env_f)
    print  ("  `uvm_info(get_type_name(), \"In build_phase\", UVM_HIGH)\n",file=env_f)
    print  ("  //if (!uvm_config_db #("+tbname+"_env_config)::get(this, \"\", \"m_env_config\", m_env_config)) ",file=env_f)
    print  ("  //  `uvm_error(get_type_name(), \"Unable to get "+tbname+"_env_config\")",file=env_f)
    for agent in agent_list: 
        print  ("  m_"+agent+"_agent = "+agent+'_agent::type_id::create("m_'+agent+'_agent", this);\n',file=env_f)

    #print >>env_f, "  m_refm   =  "+tbname+"_refm::type_id::create(\"m_refm\",this);"
    #print >>env_f, "  m_scb    =  "+tbname+"_scb::type_id::create(\"m_scb\",this);\n"
    print  ("endfunction : build_phase\n",file=env_f)

    #connect phase
    print  ("function void "+tbname+"_env::connect_phase(uvm_phase phase);\n",file=env_f)
    print  ("  `uvm_info(get_type_name(), \"In connect_phase\", UVM_HIGH)\n",file=env_f)
    print  ("endfunction : connect_phase\n",file=env_f)
    
    print  ("// Could print out diagnostic information, for example\n",file=env_f)
    print  ("function void "+tbname+"_env::end_of_elaboration_phase(uvm_phase phase);\n",file=env_f)
    print  ("  //uvm_top.print_topology();\n",file=env_f)
    print  ("  //`uvm_info(get_type_name(), $sformatf(\"Verbosity level is set to: %d\", get_report_verbosity_level()), UVM_MEDIUM)",file=env_f)
    print  ("  //`uvm_info(get_type_name(), \"Print all Factory overrides\", UVM_MEDIUM)",file=env_f)
    print  ("  //factory.print();\n",file=env_f)
    print  ("endfunction : end_of_elaboration_phase\n",file=env_f)

    print  ("`endif // "+tbname.upper()+"_ENV_SV\n\n",file=env_f)
    env_f.close();
#end def gen_top_env


def gen_top_test():
    global project
    global tbname

    dir_path = project+"/dv/tests/"
    try:
        top_test_f = open(dir_path+tbname+"_test_pkg.sv", "w" )
    except IOError:
        print ("can't open test: "+tbname+"_test_pkg.sv")

    write_file_header(top_test_f)

    print  ("`ifndef "+tbname.upper()+"_TEST_PKG_SV",file=top_test_f)
    print  ("`define "+tbname.upper()+"_TEST_PKG_SV\n",file=top_test_f)
    print  ("package "+tbname+"_test_pkg;\n",file=top_test_f)
    print  ("  `include \"uvm_macros.svh\"\n",top_test_f)
    print  ("  import uvm_pkg::*;\n",top_test_f)

    for agent in agent_list:
        print  ("  import "+agent+"_pkg::*;\n",file=top_test_f)

    print  ("  import "+tbname+"_env_pkg::*;",file=top_test_f)
    print  ("  `include \""+tbname+"_base_test.sv\"\n",top_test_f)
    print  ("endpackage : "+tbname+"_test_pkg\n",file=top_test_f)
    print  ("`endif // "+tbname.upper()+"_TEST_PKG_SV\n",file=top_test_f)
    top_test_f.close();

    # define specific tests
    try:
        base_test_f = open(dir_path+tbname+"_base_test.sv" , "w")
    except IOError:
        print ("Exiting due to Error: can't open test: "+tbname+"_base_test.sv")

    write_file_header(base_test_f)

    print  ("`ifndef "+tbname.upper()+"_BASE_TEST_SV",file=base_test_f)
    print  ("`define "+tbname.upper()+"_BASE_TEST_SV\n",file=base_test_f)

    print  ("class "+tbname+"_base_test extends uvm_test;",base_test_f)
    print  ("  `uvm_component_utils("+tbname+"_base_test)\n",base_test_f)
    print  ("  "+tbname+"_env           m_env;",base_test_f)
    print  ("  "+tbname+"_env_config    m_env_config;",base_test_f)

    for  agent in agent_list:
        print  ("  "+agent+"_agent_config  m_"+agent+"_agent_config; \n",base_test_f)
    print  ("  "+agent_list[0]+"_seq "+agent_list[0]+"_seq_i; \n",base_test_f)

    print  ("  extern function new(string name, uvm_component parent=null);",base_test_f)
    print  ("  extern function void build_phase(uvm_phase phase);",base_test_f)
    print  ("  extern function void connect_phase(uvm_phase phase);",base_test_f)
    print  ("  extern function void end_of_elaboration_phase(uvm_phase phase);",base_test_f)
    print  ("  extern task          main_phase(uvm_phase phase);\n",base_test_f)
    print  ("endclass : "+tbname+"_base_test\n",file=base_test_f)

    print  ("function "+tbname+"_base_test::new(string name, uvm_component parent=null);",base_test_f)
    print  ("  super.new(name, parent);",base_test_f)
    print  ("endfunction : new\n",base_test_f)

    print  ("function void "+tbname+"_base_test::build_phase(uvm_phase phase);",base_test_f)
    print  ("  m_env        = "+tbname+'_env::type_id::create("m_env", this);',base_test_f)
    print  ("  m_env_config    = "+tbname+'_env_config::type_id::create("m_env_config", this);',base_test_f)

    for agent in agent_list: 
        print  ("  m_"+agent+"_agent_config = "+agent+'_agent_config::type_id::create("m_'+agent+'_agent_config", this);\n',file=base_test_f)

    print  ("  file=void'(m_env_config.randomize());\n",base_test_f)
    print  ("  uvm_config_db#("+tbname+"_env_config)::set(this, \"*\", \"m_env_config\", m_env_config);\n",base_test_f)
    for agent in agent_list:
        # print (>>base_test_f, "  void'(m_"+agent+"_agent_config.randomize());\n")
        print (" uvm_config_db ", file=base_test_f) 
        #uvm_config_db#("+agent+'_agent_config)::set(this, "m_env.*", "m_'+agent+"_agent_config\", m_" + agent + '_agent_config);') #\n")

    print  ("  "+agent_list[0]+"_seq_i = "+agent_list[0]+'_seq::type_id::create("'+agent_list[0]+'_seq_i", this); \n',base_test_f)
    print  ("endfunction : build_phase\n",base_test_f)

    print  ("function void "+tbname+"_base_test::connect_phase(uvm_phase phase);\n",base_test_f)
    print  ("endfunction : connect_phase\n",base_test_f)

    print  ("function void "+tbname+"_base_test::end_of_elaboration_phase(uvm_phase phase);\n",base_test_f)
    print  ("  uvm_top.print_topology();",base_test_f)
    print  ("  `uvm_info(get_type_name(), $sformatf(\"Verbosity level is set to: %d\", get_report_verbosity_level()), UVM_MEDIUM)",base_test_f)
    print  ("  `uvm_info(get_type_name(), \"Print all Factory overrides\", UVM_MEDIUM)",base_test_f)
    print  ("  factory.print();\n",base_test_f)
    print  ("endfunction : end_of_elaboration_phase\n",base_test_f)

    print  ("task "+tbname+"_base_test::main_phase(uvm_phase phase);\n",base_test_f)
    print  ("    super.main_phase(phase);",base_test_f)
    print  ("    phase.raise_objection(this);",base_test_f)
    print  ("    //seq.starting_phase = phase;",base_test_f)
    print  ("    #10us;",base_test_f)
    print  ("    "+agent_list[0]+"_seq_i.start(m_env.m_"+agent_list[0]+"_agent.m_sequencer);",file=base_test_f)
    print  ("    `uvm_info(get_type_name(), \"Hello World!\", UVM_LOW)",base_test_f)
    print  ("    phase.drop_objection(this);",base_test_f)
    print  ("endtask : main_phase\n",base_test_f)

    print  ("`endif // "+tbname.upper()+"_BASE_TEST_SV",file=base_test_f)
    base_test_f.close();

#end def gen_test_top

def gen_top_pkg():
    global project
    global tbname

    ### file list for files in sv directoru (.svh file)
    dir_path = project+"/dv/env/"
    try:
        env_pkg_f = open( dir_path+tbname+"_env_pkg.sv", "w" )
    except IOError:
        print ("Exiting due to Error: can't open include file: $tbname")
    write_file_header(env_pkg_f)

    print  ("package "+tbname+"_env_pkg;\n\n",file=env_pkg_f)
    print  ("  `include \"uvm_macros.svh\"\n\n",env_pkg_f)
    print  ("  import uvm_pkg::*;\n\n",env_pkg_f)
    #print  ("  import regmodel_pkg::*;\n" if file=$regmodel;,env_pkg_f)

    for agent in agent_list: print  ("  import "+agent+"_pkg::*;\n",file=env_pkg_f)
    print  ("  `include \""+tbname+"_env_config.sv\"",env_pkg_f)
    print  ("  `include \""+tbname+"_refm.sv\"",env_pkg_f)
    print  ("  `include \""+tbname+"_scb.sv\"",env_pkg_f)
    print  ("  `include \""+tbname+"_env.sv\"",env_pkg_f)
    print  ("endpackage : "+tbname+"_env_pkg\n",file=env_pkg_f)
    env_pkg_f.close();


def gen_top():
    global project
    global tbname
    ### generate top modules
    ###Testbench
    dir_path = project+"/dv/tb/"          
    try:
        file_f = open(dir_path+tbname+"_tb.sv", "w" )
    except IOError:
        print ("Exiting due to Error: can't open include file: "+tbname+"_tb.sv")

    write_file_header(file_f)
    print  ("`timescale 1ns/1ns\n",file=file_f)
    print  ("module "+tbname +"_tb;\n",file=file_f)
    print  ("//  timeunit $timeunit;\n",file=file_f)
    print  ("//  timeprecision $timeprecision;\n\n",file=file_f)
    print  ("  `include \"uvm_macros.svh\"\n",file=file_f)
    print  ("  import uvm_pkg::*;\n",file=file_f)

    for agent in agent_list:
        print  ("  import "+agent+"_pkg::*;",file=file_f)
    print  ("  import "+tbname+"_test_pkg::*;",file=file_f)
    print  ("  import "+tbname+"_env_pkg::*;\n",file=file_f)

    for agent in agent_list:
        print  ("  "+agent+"_if    file=m_"+agent+"_if();\n",file=file_f)

    print  ("  ///////////////////////// \n",file=file_f)
    print  ("  //dut u_dut(*) \n",file=file_f)
    print  ("  ///////////////////////// \n",file=file_f)

    print  ("  // Example clock and reset declarations\n",file=file_f)
    print  ("  logic clock = 0;\n",file=file_f)
    print  ("  logic reset;\n",file=file_f)
    print  ("  // Example clock generator process\n",file=file_f)
    print  ("  always #10 clock = ~clock;\n",file=file_f)

    print  ("  // Example reset generator process\n",file=file_f)
    print  ("  initial\n",file=file_f)
    print  ("  begin\n",file=file_f)
    print  ("    reset = 0;         // Active low reset in this file=example\n",file=file_f)
    print  ("    #75 reset = 1;\n",file=file_f)
    print  ("  end\n",file=file_f)
    print  ("  initial\n",file=file_f)
    print  ("  begin\n",file=file_f)
    for agent in (agent_list): 
        print  ("    uvm_config_db #(virtual "+agent+'_if)::set(null, "*", "'+agent+'_vif", m_'+agent+"_if);\n",file=file_f)
    print  ("  end\n",file=file_f)

    print  ("  initial\n",file=file_f)
    print  ("  begin\n",file=file_f)
    print  ("    run_test();\n",file=file_f)
    print  ("  end\n",file=file_f)
    print  ("endmodule\n",file=file_f)
    file_f.close();


def gen_irun_script():
    dir_path = project+"/dv/sim/"
    ius_opts = "-timescale 1ns/1ns -uvm"

    try:
        ius_f = open( dir_path+"run_irun.csh", "w" )
    except IOError:
        print ("Exiting due to Error: can't open file: run_irun.csh")
    print  ("#!/bin/sh\n\n",ius_f)
    #print  ("IUS_HOME=`ncroot`\n",ius_f)
    print  ("irun "+ius_opts+" -f filelist.f -uvmhome $UVM_HOME file=\\",ius_f)
    print  ("  +UVM_TESTNAME="+tbname+"_base_test +UVM_VERBOSITY=UVM_FULL -l "+tbname+"_base_test.log\n",file=ius_f)
    gen_compile_file_list()
    ius_f.close();

    ### add execute permissions for script
    os.chmod( dir_path+"run_irun.csh", 755 )


def gen_vcs_script():
    dir_path = project+"/dv/sim/"
    vcs_f = open( dir_path+"Makefile", "w" )

    try:
        vcs_opts = "vcs -sverilog -ntb_opts uvm -debug_pp -timescale=1ns/1ns \\"
    except IOError:
        print ("Exiting due to Error: can't open file: Makefile")

    print  ("#!/bin/sh\n\n",file=vcs_f)
    print  ("RTL_PATH=../../rtl",file=vcs_f)
    print  ("TB_PATH=../../dv",file=vcs_f)
    print  ("VERB=UVM_MEDIUM",file=vcs_f)
    print  ("SEED=1",file=vcs_f)
    print  ("TEST="+tbname+"_base_test\n",file=vcs_f)
    print  ("all: comp run\n",file=vcs_f)
    
    print  ("comp:",file=vcs_f)
    print  ("\t"+vcs_opts,file=vcs_f)
    print  ("    -l comp.log\n",file=vcs_f)
    gen_compile_file_list()

    print  ("run:",file=vcs_f)
    print  ("\t./simv +UVM_TESTNAME=\${TEST} +UVM_VERBOSITY=\${VERB} +ntb_random_seed=\${SEED} -l \${TEST}.log\n",file=vcs_f)

    print  ("dve:",file=vcs_f)
    print  ("\tdve -vpd vcdplus.vpd&\n",file=vcs_f)

    print  ("clean:",file=vcs_f)
    print  ("\trm -rf csrc simv* ",file=vcs_f)

    vcs_f.close()

    ### add execute permissions for script
    os.chmod( dir_path+"Makefile", 755 );


def gen_compile_file_list():
    global project

    dir_path = project+"/dv/sim/"
    file_f = open(dir_path+"filelist.f", "w")

    incdir = ""
    for agent in agent_list:
        incdir += "  +incdir+../agent/"+agent+"\\\n"

    incdir += "  +incdir+../tb \\\n"
    incdir += "  +incdir+../env \\\n"
    incdir += "  +incdir+../agent \\\n"
    incdir += "  +incdir+../agent/uart \\\n"
    incdir += "  +incdir+../tests \\\n"
    incdir += "  +incdir+../tests/test_seq\\\n"
    incdir += "  +incdir+../ \\\n"

    print ( incdir + "", file=file_f)

    #need to compile agents before envs
    for agent in agent_list:
        print  ("  ../agent/"+agent+"/"+agent+"_pkg.sv \\\n",file=file_f)
        print  ("  ../agent/"+agent+"/"+agent+"_if.sv \\\n",file=file_f)
   
    print  ("  ../agent/"+agent_name+"/"+agent_name+"_pkg.sv \\\n",file=file_f)
    print  ("  ../env/"+tbname+"_env_pkg.sv \\",file=file_f)
    print  ("  ../tests/"+tbname+"_test_pkg.sv \\",file=file_f)
    print  ("  ../tb/"+tbname+"_tb.sv \n",file=file_f)
    file_f.close()


if __name__ == "__main__":
    tb_gen(sys.argv[1:])
