from PIL import Image
import math

# CHANGE to Vivado output hex file path
input_hex_path = "a0934-kme_390_P1.5_baseline_out.hex"
output_image_path = "a0934-kme_390_P1.5_baseline_out.png"

def generate_png():
    
    with open(input_hex_path, 'r') as file:
            lines = [line.strip() for line in file if line.strip()]

    total_pixels = len(lines)
    print(f"{total_pixels} pixels from hardware output.")
        
    # CHANGE width to match original image
    width = 700
    height = total_pixels//width
    
    # Image rebuilding 
    img = Image.new('RGB', (width, height))
    pixel_index = 0

    for y in range(height):
        for x in range(width):
            if pixel_index >= total_pixels:
                break
                
            hex_string = lines[pixel_index]
            
            r_hex = hex_string[0:2]
            g_hex = hex_string[2:4]
            b_hex = hex_string[4:6]
            
            r = int(r_hex, 16)
            g = int(g_hex, 16)
            b = int(b_hex, 16)
            
            img.putpixel((x, y), (r, g, b))
            
            pixel_index += 1

    img.save(output_image_path)
    print(f"Saved gamma-corrected image as {output_image_path} ({width}x{height})")

if __name__ == "__main__":
    generate_png()