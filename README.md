# Typisch Ich Motive Collage Generator
Diese WebApp erstellt die Collagen für die Produkt Bilder von Typisch Ich.

## Verwendung
Webseite ist ereichbar unter: [motive-collage-generator.typischich.shop](https://motive-collage-generator.typischich.shop/)

**Studio3 zu PNG**

1. Design in Silhouette Studio öffnen und lokal speichern
   Datei → Sichern als → Auf der Festplatte speichern --→rt auswählen
2. Die .studio3 Dateien mit der Webseite [Studio zu SVG Converter](http://www.ideas-r-us-software.uk/FileConverters/SilhouetteStudioConverter.aspx) zu einem SVG umwandeln
3. Die umgewandelten SVG Dateien hier auf der Webseite unter `SVG in PNG konvertieren`
 bei `Dateien hochladen` hochladen und dann auf den Button `konvertieren` klicken
4. Das ZIP `TypischIch_ConvertedPNGs.zip` extrahieren und die PNGs zu den anderen verschieben

**Collage Generator**

5. Alle Motive im Format PNG hier auf der Webseite unter `Collage generieren` bei `Dateien hochladen` hochladen und dann auf den Button `Collagen generieren` klicken
6. Das ZIP `TypischIch_MotiveCollages.zip` extrahieren und auf die Webseite hochladen

## Deplyoment
Bei einem Push in den Main Branach wird mit dem [Dockerfile](Dockerfile) ein Image erstellt und in das [Docker Hub Repository](https://hub.docker.com/repository/docker/surmatik/typischich-motivecollagegenerator/) gepusht.

Das Docker Image kann dadurch via Docker Compose deployed werden.
```sh
version: '3'

services:
  typischich-motivecollagegenerator:
    image: surmatik/typischich-motivecollagegenerator:latest
    ports:
      - "5000:5000"
```

## Run local
[Python3](https://www.python.org/downloads/) muss installiert sein
1. Github Repository klonen
   ```sh
   git clone https://github.com/surmatik/TypischIch-MotiveCollageGenerator.git
   ```
2. Installiere die erforderlichen Python-Pakete:
   ```sh
   pip install -r requirements.txt
   ```
3. Installiere die erforderlichen Python-Pakete:
   ```sh
   python3 app.py
   ```