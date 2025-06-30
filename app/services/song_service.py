# song_service.py

import os
from datetime import datetime
from flask import Flask, Response

# Inicializa una aplicación Flask que actuará como microservicio para consultar la última canción reproducida
app = Flask(__name__)


def get_last_song():
    """
    Obtiene la última canción reproducida desde el archivo de log de OtsAV.

    El archivo esperado debe estar ubicado en:
    C:/OtsLabs/Logs/YYYY-MM-DD-playlog.txt

    Se espera que cada línea del archivo tenga un formato similar a:
    04-Jun-2025 07:02:20 La Sonora Dinamita - El Desamor Otsav

    :return: string con formato "Artista - Título", o None si hay un error
    """
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = f"C:/OtsLabs/Logs/{today}-playlog.txt"

    if not os.path.isfile(log_file):
        print(f"[ERROR] Log file not found: {log_file}")
        return None

    try:
        # Codificación 'latin-1' usada para evitar errores por caracteres especiales del log
        with open(log_file, "r", encoding="latin-1") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"[ERROR] Failed to read log file: {e}")
        return None

    if not lines:
        print("[WARNING] Log file is empty.")
        return None

    last_line = lines[-1].strip()
    try:
        # Extrae "Artista - Título" antes de "Otsav"
        song_info = last_line.split(" ", 2)[2]
        artist_title = song_info.rsplit("Otsav", 1)[0].strip()
        artist, title = artist_title.split(" - ", 1)
        return f"{artist.strip()} - {title.strip()}"
    except Exception as e:
        print(f"[ERROR] Failed to parse last line: {e}")
        print(f"[DEBUG] Raw line: {last_line}")
        return None


@app.route("/current_song.txt")
def current_song():
    """
    Ruta HTTP que responde con el nombre de la última canción reproducida.
    """
    title = get_last_song()
    if title:
        return Response(title, mimetype="text/plain")
    return Response("Lanceros Stereo 94.1 FM", mimetype="text/plain")


def start_song_server():
    """
    Inicia el servidor Flask en segundo plano.
    Ideal para integrarse como hilo en la interfaz principal del programa.
    """
    print("🎵 Iniciando servidor Flask para mostrar canción actual...")
    app.run(host="0.0.0.0", port=8080)
