# Basis-Image auswählen
FROM python:3.10

# Arbeitsverzeichnis im Container erstellen
WORKDIR /app

# Kopiere die Projektdateien in das Arbeitsverzeichnis im Container
COPY app.py requirements.txt /app/
COPY templates /app/templates
COPY assets /app/assets

RUN pip install --upgrade Flask Werkzeug

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install gunicorn

# Port, den der Container freigeben soll
EXPOSE 5000

# Befehl, der ausgeführt wird, wenn der Container gestartet wird
CMD ["gunicorn", "--worker-class", "gevent", "--bind", "0.0.0.0:5000", "app:app"]