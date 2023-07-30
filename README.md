# Typisch Ich Motive Collage Generator
Dieser Script [script.js](script.py) erstellt aus allen Motiven im Ordner [motive](motive) eine Collage im Format von 3 x 4, um diese dann für die Produkt Bilder auf typischich.shop verwenden zu können.

## Voraussetzungen
Folgende Bibliotheken müssen für den Python Script installiert sein:
- Python 3.x --> [Python Download](https://www.python.org/downloads/)
- Pillow (Python Imaging Library) --> `pip install pillow`

## Verwendung
1. Lege alle Motive im Ordner [motive](motive) als PNG ab
2. Führe das Skript [script.js](script.py) aus
    ```sh
    python3 script.py
    ```

## Anpassung
Folgene Parameter im Skript könenn angepasst werden, um das Erscheinungsbild der Collagen zu ändern:

- spacing: Der Abstand (in Pixeln) zwischen den Bildern in der Collage.
- margin: Der Randabstand (in Pixeln) der Collage.
- image_width: Die Breite der Bilder in der Collage (die Höhe wird automatisch angepasst).
- image_height: Die maximale Höhe der Bilder in der Collage. Die Höhe des Collage-Feldes für den Bildtitel bleibt unverändert.
- title_height: Die Höhe des Feldes für den Bildtitel unter jedem Bild.
- watermark_path: Der Dateipfad zum Wasserzeichenbild (standardmäßig "assets/wasserzeichen.png").
- opacity: Die Transparenz des Wasserzeichens (Wert zwischen 0.0 und 1.0).