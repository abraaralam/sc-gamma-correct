# Generate SAIF for power data

# IMPORTANT: to generate SAIF comparison files: 

#  - Stochastic: in tb/tb_gamma_top.sv change UUT to gamma_top,
#                in THIS FILE set SAIF_FILE to sc_power.saif
#                in scripts/power_sim.tcl set open_saif to sc_power.saif

#  - Baseline:   in tb/tb_gamma_top.sv change UUT to baseline_non_sc,
#                in THIS FILE set SAIF_FILE to baseline_power.saif
#                in scripts/power_sim.tcl set open_saif to baseline_power.saif

# Open resulting file in Vivado in power report configuration after Implementation 

import os
import subprocess
from PIL import Image

# Points to test image
TARGET_IMAGE = "/home/abraar/gamma/images/test_directory/OverExposed/a0209-_DGW6273_P1.5.JPG"
INPUT_HEX = "input_image.hex"
TARGET_RES = 256

SAIF_FILE = "baseline_power.saif" # Change depending on UUT
TCL_SCRIPT = "scripts/power_sim.tcl"

def generate_power_saif():
    print(f"Generating power profile using specific image: {TARGET_IMAGE}")

    # Center-crop + convert to hex
    img = Image.open(TARGET_IMAGE).convert('RGB')
    width, height = img.size
    left = (width - TARGET_RES) // 2
    top = (height - TARGET_RES) // 2
    right = (width + TARGET_RES) // 2
    bottom = (height + TARGET_RES) // 2
    img = img.crop((left, top, right, bottom))

    with open(INPUT_HEX, 'w') as f:
        for y in range(TARGET_RES):
            for x in range(TARGET_RES):
                r, g, b = img.getpixel((x, y))
                f.write(f"{r:02x}{g:02x}{b:02x}\n")

    # Tcl script generated with each run
    with open(TCL_SCRIPT, 'w') as f:
        f.write(f"open_saif {SAIF_FILE}\n")
        f.write("log_saif [get_objects -r /tb_gamma_top/uut/*]\n")
        f.write("run all\n")
        f.write("close_saif\n")
        f.write("quit\n")

    print("Compiling RTL...")
    subprocess.run(["xvlog", "-sv", "hdl/gamma_top.sv", "hdl/sng.sv", "hdl/lfsr_8bit.sv", "hdl/baseline_non_sc.sv", "tb/tb_gamma_top.sv"], check=True)
    subprocess.run(["xelab", "-debug", "typical", "-top", "tb_gamma_top", "-snapshot", "tb_sim"], check=True)
    
    print(f"\nExecuting hardware simulation (this will take ~1 minute for SC, ~1 second for baseline)...")
    subprocess.run(["xsim", "tb_sim", "-R", "-tclbatch", TCL_SCRIPT])
    
    print(f"\nPower analysis data saved to {SAIF_FILE}")

if __name__ == "__main__":
    generate_power_saif()