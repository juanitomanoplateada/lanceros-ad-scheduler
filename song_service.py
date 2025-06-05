# song_service.py
import os
from datetime import datetime
from flask import Flask, Response

app = Flask(__name__)

def get_last_song():
    today = datetime.now().strftime("%Y-%m-%d")
    print(today)
    log_file = f"C:/OtsLabs/Logs/{today}-playlog.txt"

    if not os.path.isfile(log_file):
        print(f"[ERROR] Log file not found: {log_file}")
        return None

    try:
        with open(log_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        print(f"[ERROR] Failed to read log file: {e}")
        return None

    if not lines:
        print("[WARNING] Log file is empty.")
        return None

    last_line = lines[-1].strip()
    try:
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
    title = get_last_song()
    if title:
        return Response(title, mimetype="text/plain")
    return Response("Lanceros Stereo 94.1 FM", mimetype="text/plain")

def start_song_server():
    print("🎵 Iniciando servidor Flask para mostrar canción actual...")
    app.run(host="0.0.0.0", port=8080)
