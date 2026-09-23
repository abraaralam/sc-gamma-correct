# Change depending on UUT
open_saif baseline_power.saif
log_saif [get_objects -r /tb_gamma_top/uut/*]
run all
close_saif
quit
