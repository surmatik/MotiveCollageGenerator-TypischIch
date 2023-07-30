import os
import math
from PIL import Image, ImageDraw

def create_collage(images):
    # Berechnen der Anzahl der Reihen und Spalten für die Collage (4x3)
    rows = 4
    cols = 3
    collage_width = 300 * cols  # 300 ist die Breite jedes Bildes
    collage_height = 400 * rows  # 400 ist die Höhe jedes Bildes

    collage = Image.new('RGB', (collage_width, collage_height), color='black')
    draw = ImageDraw.Draw(collage)

    for i, image in enumerate(images):
        row = i // cols
        col = i % cols
        x = col * 300  # 300 ist die Breite jedes Bildes
        y = row * 400  # 400 ist die Höhe jedes Bildes
        collage.paste(image, (x, y))

    return collage

def main():
    # Ordnerpfad mit den PNG-Dateien
    folder_path = 'motives'
    file_names = sorted([f for f in os.listdir(folder_path) if f.endswith('.png')])

    images = []
    for file_name in file_names:
        image_path = os.path.join(folder_path, file_name)
        image = Image.open(image_path)
        images.append(image)

    # Anzahl der benötigten Collagen berechnen
    num_collages = math.ceil(len(images) / 12)  # 12 Bilder pro Collage (4x3)

    for i in range(num_collages):
        collage_images = images[i * 12: (i + 1) * 12]
        collage = create_collage(collage_images)

        # Collage speichern
        collage.save(f'collage_{i+1}.png')

if __name__ == '__main__':
    main()
