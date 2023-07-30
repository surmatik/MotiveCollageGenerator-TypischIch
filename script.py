import os
import math
from PIL import Image, ImageDraw

def create_collage(images, spacing=30, margin=30):
    # Berechnen der Anzahl der Reihen und Spalten für die Collage (3x4)
    rows = 3
    cols = 4
    image_width = 300
    image_height = 400
    collage_width = image_width * cols + spacing * (cols - 1) + 2 * margin
    collage_height = image_height * rows + spacing * (rows - 1) + 2 * margin

    collage = Image.new('RGB', (collage_width, collage_height), color='black')

    for i, image in enumerate(images):
        if not isinstance(image, Image.Image):
            # Falls es kein gültiges Bildobjekt ist, überspringen und warnen
            print(f"Warnung: {image} ist kein gültiges Bildobjekt und wird übersprungen.")
            continue

        row = i // cols
        col = i % cols
        x = col * (image_width + spacing) + margin
        y = row * (image_height + spacing) + margin

        # Bild in der Collage einfügen und auf die richtige Größe skalieren
        image.thumbnail((image_width, image_height))
        offset_x = (image_width - image.width) // 2
        offset_y = (image_height - image.height) // 2
        collage.paste(image, (x + offset_x, y + offset_y))

    # Graue horizontale Linien zwischen den Bildern hinzufügen
    draw = ImageDraw.Draw(collage)
    for i in range(1, rows):
        y = i * (image_height + spacing) + margin - spacing // 2
        draw.line((margin, y, collage_width - margin, y), fill='gray', width=10)

    return collage

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

        # Collage speichern
        collage.save(f'collage_{i+1}.png')

if __name__ == '__main__':
    main()
