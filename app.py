import os
import math
import zipfile
import shutil
import cairosvg
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from flask import Flask, render_template, request, send_file
from urllib.parse import quote as url_quote

app = Flask(__name__)

def create_collage(images, image_paths, spacing=90, margin=90):
    rows = 3
    cols = 4
    image_width = 340
    image_height = 300
    title_height = 40
    collage_width = image_width * cols + spacing * (cols - 1) + 2 * margin
    collage_height = image_height * rows + spacing * (rows - 1) + 2 * margin + title_height

    collage = Image.new('RGB', (collage_width, collage_height), color='black')
    draw = ImageDraw.Draw(collage)

    for i, (image, image_path) in enumerate(zip(images, image_paths)):
        if not isinstance(image, Image.Image):
            print(f"Warning: {image} is not a valid image object and will be skipped.")
            continue

        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Resize the image
        image.thumbnail((image_width, image_height))

        row = i // cols
        col = i % cols
        x = col * (image_width + spacing) + margin
        y = row * (image_height + spacing) + margin

        offset_x = (image_width - image.width) // 2
        offset_y = (image_height - image.height) // 2
        collage.paste(image, (x + offset_x, y + offset_y))

        # Draw the file name below the image
        font_size = 25
        font = ImageFont.truetype("assets/SansSerifBldFLF.otf", font_size)
        file_name = os.path.splitext(os.path.basename(image_path))[0]
        text_bbox = draw.textbbox((x, y + image_height, x + image_width, y + image_height + title_height), file_name, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = x + (image_width - text_width) // 2
        text_y = y + image_height + (title_height // 2) - (text_height // 2)
        draw.text((text_x, text_y), file_name, fill='white', font=font)

    # Draw lines between rows
    for i in range(1, rows):
        y = i * (image_height + spacing) + margin - spacing // 2
        draw.line((margin, y, collage_width - margin, y), fill='gray', width=10)

    return collage



def add_watermark(collage, watermark_path, opacity=0.5):
    # Open the watermark and resize it
    watermark = Image.open(watermark_path).convert("RGBA")
    watermark_size = (int(collage.width * 0.75), int(collage.height * 1))
    watermark = watermark.resize(watermark_size, Image.LANCZOS)

    # Apply opacity to the watermark
    watermark = watermark.convert("RGBA")
    alpha = watermark.split()[3]  # Extract the alpha channel
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)  # Modify transparency
    watermark.putalpha(alpha)

    # Paste the watermark onto the collage
    collage.paste(watermark, ((collage.width - watermark.width) // 2, 
                              (collage.height - watermark.height) // 2), watermark)
    
    # Close the watermark image to free memory
    watermark.close()


def convert_svg_to_png(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".svg"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.replace(".svg", ".png"))

            try:
                dpi = 150
                cairosvg.svg2png(url=input_path, write_to=output_path, dpi=dpi)

                image = Image.open(output_path)
                bbox = image.getbbox()
                if bbox:
                    cropped_image = image.crop(bbox)
                    cropped_image.save(output_path, dpi=(dpi, dpi))

                image.close()
            except Exception as e:
                print(f"Failed to convert {input_path}: {e}")

def save_filenames_to_txt(image_paths):
    with open('Liste_Motive.txt', 'w') as txt_file:
        txt_file.write("Wähle ein Hobby aus|Wähle ein Hobby aus\n")
        for image_path in image_paths:
            filename = os.path.splitext(os.path.basename(image_path))[0]
            txt_file.write(f"{filename}|{filename}\n")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Collage generation
        uploaded_files = request.files.getlist('file')
        temp_dir = 'temp'
        os.makedirs(temp_dir, exist_ok=True)
        image_paths = []
        for file in uploaded_files:
            if file.filename != '':
                file_path = os.path.join(temp_dir, file.filename)
                file.save(file_path)
                image_paths.append(file_path)

        # Sort the image paths alphabetically
        image_paths.sort(key=lambda path: os.path.basename(path).lower())

        num_collages = math.ceil(len(image_paths) / 12)

        collage_paths = []
        for i in range(num_collages):
            collage_images = [Image.open(img) for img in image_paths[i * 12: (i + 1) * 12]]
            collage = create_collage(collage_images, image_paths[i * 12: (i + 1) * 12])

            watermark_path = 'assets/wasserzeichen.png'
            add_watermark(collage, watermark_path, opacity=0.8)

            collage_path = os.path.join(temp_dir, f'collage_{i+1}.png')  # Collage file path in the temp folder
            collage.save(collage_path)
            collage_paths.append(collage_path)

        # Save file names to TXT
        save_filenames_to_txt(image_paths)

        # Create ZIP file with the collages
        zip_file_path = 'TypischIch_MotiveCollages.zip'
        with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
            for path in collage_paths:
                zip_file.write(path, os.path.basename(path))
            zip_file.write('Liste_Motive.txt')  # Add file names

        # Delete temporary files
        for path in collage_paths:
            os.remove(path)
        os.remove('Liste_Motive.txt')
        
        # Download ZIP file
        return send_file(zip_file_path, as_attachment=True)

    return render_template('index.html')

@app.route('/convert_svg', methods=['POST'])
def convert_svg():
    uploaded_files = request.files.getlist('svg_file')
    svg_input_folder = 'svg'
    os.makedirs(svg_input_folder, exist_ok=True)
    for file in uploaded_files:
        if file.filename != '':
            file_path = os.path.join(svg_input_folder, file.filename)
            file.save(file_path)

    png_output_folder = 'png'
    convert_svg_to_png(svg_input_folder, png_output_folder)

    # Erstelle eine ZIP-Datei mit den konvertierten PNGs
    zip_file_path = 'TypischIch_ConvertedPNGs.zip'
    with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
        for png_file in os.listdir(png_output_folder):
            zip_file.write(os.path.join(png_output_folder, png_file))

    # Lösche temporäre Ordner
    shutil.rmtree(svg_input_folder)
    shutil.rmtree(png_output_folder)

    # ZIP-Datei herunterladen
    return send_file(zip_file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
