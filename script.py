import os
import math
from PIL import Image, ImageDraw, ImageFont

def create_collage(images, spacing=90, margin=90):
    # Berechnen der Anzahl der Reihen und Spalten für die Collage (3x4)
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
            # Falls es kein gültiges Bildobjekt ist, überspringen und warnen
            print(f"Warnung: {image} ist kein gültiges Bildobjekt und wird übersprungen.")
            continue

        # Konvertiere das Bild in den RGBA-Modus, falls es im Palette-Modus mit Transparenz vorliegt
        if image.mode == 'P' and 'transparency' in image.info:
            image = image.convert('RGBA')

        row = i // cols
        col = i % cols
        x = col * (image_width + spacing) + margin
        y = row * (image_height + spacing) + margin

        # Bild in der Collage einfügen und auf die richtige Größe skalieren
        image.thumbnail((image_width, image_height))
        offset_x = (image_width - image.width) // 2
        offset_y = (image_height - image.height) // 2
        collage.paste(image, (x + offset_x, y + offset_y))

        # Bildtitel hinzufügen
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

    # Graue horizontale Linien zwischen den Bildern hinzufügen
    draw = ImageDraw.Draw(collage)
    for i in range(1, rows):
        y = i * (image_height + spacing) + margin - spacing // 2
        draw.line((margin, y, collage_width - margin, y), fill='gray', width=10)

    return collage

def add_watermark(collage, watermark_path, opacity=0.5):
    # Öffne das Wasserzeichenbild
    watermark = Image.open(watermark_path)

    # Vergrößere das Wasserzeichen auf das 1.5-fache der Collage-Größe
    watermark_size = (int(collage.width * 0.75), int(collage.height * 1))
    watermark = watermark.resize(watermark_size, Image.LANCZOS)

    # Passe die Transparenz des Wasserzeichens an
    if opacity < 0.0:
        opacity = 0.0
    elif opacity > 1.0:
        opacity = 1.0
    watermark = watermark.convert('RGBA')
    watermark_with_opacity = Image.new('RGBA', collage.size, (0, 0, 0, 0))
    
    # Berechne die Position des Wasserzeichens in der Mitte der Collage
    x = (collage.width - watermark.width) // 2
    y = (collage.height - watermark.height) // 2

    # Füge das Wasserzeichen zur Collage hinzu
    for x_offset in range(watermark.width):
        for y_offset in range(watermark.height):
            r, g, b, a = watermark.getpixel((x_offset, y_offset))
            watermark_with_opacity.putpixel((x + x_offset, y + y_offset), (r, g, b, int(a * opacity)))
    
    collage.paste(watermark_with_opacity, (0, 0), watermark_with_opacity)

def main():
    # Ordnerpfad mit den Dateien
    folder_path = 'motive'
    file_names = sorted([f for f in os.listdir(folder_path) if f.endswith('.png')])

    images = []
    for file_name in file_names:
        image_path = os.path.join(folder_path, file_name)
        try:
            image = Image.open(image_path)
            images.append(image)
        except Exception as e:
            print(f"Fehler beim Laden von {image_path}: {e}")

    # Anzahl der benötigten Collagen berechnen
    num_collages = math.ceil(len(images) / 12)  # 12 Bilder pro Collage (3x4)

    for i in range(num_collages):
        collage_images = images[i * 12: (i + 1) * 12]
        collage = create_collage(collage_images)

        # Wasserzeichen hinzufügen (angepasst nach Bedarf)
        watermark_path = 'assets/wasserzeichen.png'
        add_watermark(collage, watermark_path, opacity=0.8)

        # Collage speichern
        collage.save(f'export/collage_{i+1}.png')

if __name__ == '__main__':
    main()
