import os
import cairosvg
from PIL import Image

def convert_svg_to_png(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".svg"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.replace(".svg", ".png"))

            print(f"Converting and cropping {input_path} to {output_path}")

            try:
                dpi = 300  # Set the DPI to increase the output resolution

                # Convert SVG to PNG
                cairosvg.svg2png(url=input_path, write_to=output_path, dpi=dpi)

                # Crop the PNG to remove the surrounding whitespace
                image = Image.open(output_path)
                bbox = image.getbbox()
                cropped_image = image.crop(bbox)
                cropped_image.save(output_path, dpi=(dpi, dpi))
            except Exception as e:
                print(f"Failed to convert {input_path}: {e}")

if __name__ == "__main__":
    input_folder = "svg"  # Ändere dies zum Pfad deines SVG-Ordners
    output_folder = "png"  # Ändere dies zum Pfad deines gewünschten PNG-Ausgabeordners

    convert_svg_to_png(input_folder, output_folder)
