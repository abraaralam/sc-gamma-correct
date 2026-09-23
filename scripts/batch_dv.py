# Automated batch stochastic error verification pipeline

# Prints Average hardware error to terminal for all images in dataset.

# IMPORTANT: Before running, make sure UUT in tb/tb_gamma_top.sv is gamma_top
#            testing stochastic, set UUT to baseline_non_sc otherwise

import os
import subprocess
from PIL import Image

TEST_DIR = "images/test_directory/OverExposed"
OUTPUT_DIR = "images/output_hardware"
INPUT_HEX = "input_image.hex"
OUTPUT_HEX = "output_image.hex"
TARGET_RES = 256

os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_dv_pipeline():
    images = [f for f in os.listdir(TEST_DIR)]

    print("Compiling RTL...")
    subprocess.run(["xvlog", "-sv", "hdl/gamma_top.sv", "hdl/sng.sv", "hdl/lfsr_8bit.sv", "hdl/baseline_non_sc.sv", "tb/tb_gamma_top.sv"], check=True)
    subprocess.run(["xelab", "-debug", "typical", "-top", "tb_gamma_top", "-snapshot", "tb_sim"], check=True)

    total_dataset_error = 0
    successful_images = 0

    for img_name in images:
        print(f"\nProcessing {img_name}...")
        
        img = Image.open(os.path.join(TEST_DIR, img_name)).convert('RGB')
        
        # Image centering patch
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
        
        # Vivado call
        subprocess.run(["xsim", "tb_sim", "-R"])
        
        img_error = process_hardware_output(img, img_name)
        total_dataset_error += img_error
        successful_images += 1

    
    final_avg_error = total_dataset_error / successful_images
    
    print("\nDATASET VERIFICATION COMPLETE")
    print(f"Total Images Processed: {successful_images}")
    print(f"Final Average Hardware Error: {final_avg_error:.4f} intensity levels\n")

def process_hardware_output(original_img, img_name):
    with open(OUTPUT_HEX, 'r') as f:
            lines = [line.strip() for line in f]

    hw_img = Image.new('RGB', (TARGET_RES, TARGET_RES))
    pixels = hw_img.load()
    
    total_error = 0
    pixel_count = TARGET_RES * TARGET_RES

    for i in range(pixel_count):
        y = i // TARGET_RES
        x = i % TARGET_RES
        
        hw_hex = lines[i]
        hw_r = int(hw_hex[0:2], 16)
        hw_g = int(hw_hex[2:4], 16)
        hw_b = int(hw_hex[4:6], 16)
        
        pixels[x, y] = (hw_r, hw_g, hw_b)
        
        sw_r_input = original_img.getpixel((x, y))[0]
        sw_r_expected = (sw_r_input ** 2) // 255
        
        total_error += abs(hw_r - sw_r_expected)

    output_filename = os.path.splitext(img_name)[0] + "_corrected.png"
    hw_img.save(os.path.join(OUTPUT_DIR, output_filename))

    avg_error = total_error / pixel_count
    print(f"  -> Hardware Error vs Software Baseline: {avg_error:.4f} intensity levels")
    print(f"  -> Output saved to {OUTPUT_DIR}/{output_filename}")
    
    return avg_error

if __name__ == "__main__":
    run_dv_pipeline()