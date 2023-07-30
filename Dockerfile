# Basis-Image auswählen
FROM python:3.10

# Arbeitsverzeichnis im Container erstellen
WORKDIR /app

# Kopiere die Projektdateien in das Arbeitsverzeichnis im Container
COPY app.py requirements.txt /app/
COPY templates /app/templates
COPY assets /app/assets

# Installiere die Python-Abhängigkeiten
RUN pip install --no-cache-dir -r requirements.txt

# Port, den der Container freigeben soll
EXPOSE 5000

# Befehl, der ausgeführt wird, wenn der Container gestartet wird
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:5000", "--workers=4"]
