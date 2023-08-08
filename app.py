import os
import math
import zipfile
import shutil
import cairosvg
from PIL import Image, ImageDraw, ImageFont
from flask import Flask, render_template, request, send_file

app = Flask(__name__, static_folder='static')

def create_collage(images, spacing=90, margin=90):
    rows = 3
    cols = 4
    image_width = 340
    image_height = 300
    title_height = 40
    collage_width = image_width * cols + spacing * (cols - 1) + 2 * margin
    collage_height = image_height * rows + spacing * (rows - 1) + 2 * margin + title_height

    collage = Image.new('RGB', (collage_width, collage_height), color='black')

    for i, image in enumerate(images):
        if not isinstance(image, Image.Image):
            print(f"Warnung: {image} ist kein gültiges Bildobjekt und wird übersprungen.")
            continue

        if image.mode == 'P' and 'transparency' in image.info:
            image = image.convert('RGBA')

        row = i // cols
        col = i % cols
        x = col * (image_width + spacing) + margin
        y = row * (image_height + spacing) + margin

        image.thumbnail((image_width, image_height))
        offset_x = (image_width - image.width) // 2
        offset_y = (image_height - image.height) // 2
        collage.paste(image, (x + offset_x, y + offset_y))

        draw = ImageDraw.Draw(collage)
        font_size = 25
        font = ImageFont.truetype("assets/SansSerifBldFLF.otf", font_size)
        file_name = os.path.splitext(os.path.basename(image.filename))[0]
        text_bbox = draw.textbbox((x, y + image_height, x + image_width, y + image_height + title_height), file_name, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_x = x + (image_width - text_width) // 2
        text_y = y + image_height + title_height // 2 - text_height // 2
        draw.text((text_x, text_y), file_name, fill='white', font=font)

    draw = ImageDraw.Draw(collage)
    for i in range(1, rows):
        y = i * (image_height + spacing) + margin - spacing // 2
        draw.line((margin, y, collage_width - margin, y), fill='gray', width=10)

    return collage

def add_watermark(collage, watermark_path, opacity=0.5):
    watermark = Image.open(watermark_path)
    watermark_size = (int(collage.width * 0.75), int(collage.height * 1))
    watermark = watermark.resize(watermark_size, Image.LANCZOS)

    if opacity < 0.0:
        opacity = 0.0
    elif opacity > 1.0:
        opacity = 1.0
    watermark = watermark.convert('RGBA')
    watermark_with_opacity = Image.new('RGBA', collage.size, (0, 0, 0, 0))
    
    x = (collage.width - watermark.width) // 2
    y = (collage.height - watermark.height) // 2

    for x_offset in range(watermark.width):
        for y_offset in range(watermark.height):
            r, g, b, a = watermark.getpixel((x_offset, y_offset))
            watermark_with_opacity.putpixel((x + x_offset, y + y_offset), (r, g, b, int(a * opacity)))
    
    collage.paste(watermark_with_opacity, (0, 0), watermark_with_opacity)

def convert_svg_to_png(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(".svg"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename.replace(".svg", ".png"))

            print(f"Converting and cropping {input_path} to {output_path}")

            try:
                dpi = 300
                cairosvg.svg2png(url=input_path, write_to=output_path, dpi=dpi)

                image = Image.open(output_path)
                bbox = image.getbbox()
                cropped_image = image.crop(bbox)
                cropped_image.save(output_path, dpi=(dpi, dpi))
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
        # Collage generieren
        uploaded_files = request.files.getlist('file')
        temp_dir = 'temp'
        os.makedirs(temp_dir, exist_ok=True)
        image_paths = []
        for file in uploaded_files:
            if file.filename != '':
                file_path = os.path.join(temp_dir, file.filename)
                file.save(file_path)
                image_paths.append(file_path)

        # Sortiere die Liste der Bildpfade nach dem ABC
        image_paths.sort(key=lambda path: os.path.basename(path).lower())

        num_collages = math.ceil(len(image_paths) / 12)

        collage_paths = []
        for i in range(num_collages):
            collage_images = image_paths[i * 12: (i + 1) * 12]
            collage = create_collage([Image.open(img) for img in collage_images])

            watermark_path = 'assets/wasserzeichen.png'
            add_watermark(collage, watermark_path, opacity=0.8)

            collage_path = os.path.join(temp_dir, f'collage_{i+1}.png')  # Collagen-Dateipfad im temp-Ordner
            collage.save(collage_path)
            collage_paths.append(collage_path)

        # Dateinamen in TXT-Datei speichern
        save_filenames_to_txt(image_paths)

        # Collage ZIP erstellen
        zip_file_path = 'TypischIch_MotiveCollages.zip'
        with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
            # Füge Collage-Bilder direkt zum ZIP hinzu (ohne temp-Ordner)
            for path in collage_paths:
                zip_file.write(path, os.path.basename(path))
            zip_file.write('Liste_Motive.txt')  # Dateinamen hinzufügen

        # Temporäre Dateien löschen
        for path in collage_paths:
            os.remove(path)
        os.remove('Liste_Motive.txt')
        
        # ZIP-Datei herunterladen
        return send_file(zip_file_path, as_attachment=True)

    return render_template('index.html', page_title='Motive Collage Generator')

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

@app.route('/svg-to-png')
def pagesvgtopng():
    return render_template('svg-to-png.html', page_title='SVG zu PNG konvertieren')

@app.route('/collage-generieren')
def pagecollagegenerieren():
    return render_template('collage-generieren.html', page_title='Collage Generieren')

@app.route('/hilfe')
def pagehilfe():
    return render_template('hilfe.html', page_title='Hilfe')

app.static_folder = 'static'
app.static_url_path = '/static'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)