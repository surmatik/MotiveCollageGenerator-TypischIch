# Typisch Ich Motive Collage Generator
Dieser Script [script.js](script.py) erstellt aus allen Motiven im Ordner [motive](motive) eine Collage im Format von 3 x 4, um diese dann für die Produkt Bilder auf typischich.shop verwenden zu können.

## Verwendung
1. Github Repository klonen
   ```sh
   git clone https://github.com/surmatik/TypischIch-MotiveCollageGenerator.git
   ```
Für die Collage werden richtig zugeschnittene PNGs von den Studio3 Dateien benötigt.

### Studio3 zu PNG
2. Die Motive in Silhouette Studio auf der Festplatte speichern
3. Die .studio3 Dateien mit der Webseite [Studio zu SVG Converter](http://www.ideas-r-us-software.uk/FileConverters/SilhouetteStudioConverter.aspx) zu einem SVG umwandeln und diese dann im Ordner [svg-to-png/svg](svg-to-png/svg) von diesem Repository abspeichern
4. Den SVG zu PNG script [svg-to-png/script.py](svg-to-png/script.py) ausführen
   Für den Script muss [Python 3.x](https://www.python.org/downloads/) und die zwei Bibliotheken `cairosvg` und `Pillow` installiert sein
   ```sh
   pip install cairosvg pillow

   python3 script.py
   ```
### Collage Generator
5. Mit den PNGs kann nun auf der Webseite [motive-collage-generator.typischich.shop](https://motive-collage-generator.typischich.shop/) oder via Script [script.py](script.py) die Collagen generiert werden
   Für den Script muss [Python 3.x](https://www.python.org/downloads/) und die Bibliothek `Pillow` installiert sein
   ```sh
   pip install pillow

   python3 script.py
   ```
