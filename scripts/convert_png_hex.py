from PIL import Image

# CHANGE to image path
input_image_path = "a0934-kme_390_P1.5.png"
output_hex_path = "a0934-kme_390_P1.5_baseline_in.hex"

def generate_hex():
    
    img = Image.open(input_image_path).convert('RGB')

    width, height = img.size
    print(f"Opened image is {width}x{height} pixels")
    
    with open(output_hex_path, 'w') as hex_file:
        
        for y in range(height):
            for x in range(width):
                
                r, g, b = img.getpixel((x, y))
                hex_string = f"{r:02X}{g:02X}{b:02X}\n"
                
                # Write it to the file
                hex_file.write(hex_string)

    print(f"Wrote {width * height} pixels to {output_hex_path}")

if __name__ == "__main__":
    generate_hex()